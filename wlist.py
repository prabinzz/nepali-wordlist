#! /usr/bin/python3

import argparse
import sys
import os
import threading
import time

def arg_init():
	"""
	Argument handler (argparse) function.
	"""
	parser = argparse.ArgumentParser(description="""Usages: This script can be used to filter wordlist file according to your needs.If you need any help  contact me <prabinparajuli92@gmail.com>.""")
	parser.add_argument("wordlist",help="Wordlist to work with",type=str)
	
	parser.add_argument('-w',"--word",help="Look for specific word (',' to seperate words)",type=str)
	parser.add_argument("-o","--out",help="Output file")
	parser.add_argument("-c","--no-case",help="Ignore case matching",action="store_true")
	parser.add_argument("--sort",help="Sort wordlist before reading and outputing",action='store_true')
	parser.add_argument('--check',help="Check in the output file for word and append if not found. (Slow performance)"
		, action='store_true')

	parser.add_argument("--min",help="Minimun length of word",type=int)
	parser.add_argument("--max",help="Maximum length of word",type=int)
	parser.add_argument("--start",help="Match starting of word")
	parser.add_argument("--end",help="match end of word")
	parser.add_argument("--no-num",help="Ignore words containing numbers",
	action="store_true")

	display_mode=parser.add_mutually_exclusive_group()

	display_mode.add_argument("-v",'--verbose',help="Verbose mode",action="store_true")
	display_mode.add_argument("-s","--silent",help="Silent mod", action="store_true")

	return parser.parse_args()

def output_f(text,type="normal"):
	"""
	Formated output function.
	"""
	if type=="progress":
		print("[+] "+text)
		return
	if type=="warn":
		print("[!] "+text)
		return
	if type=="info":
		print("[?] "+text)
		return
	if type=="error":
		print("[*] "+text)
		return
	if type=="stat":
		print('-'*(len(text)+10))
		print(text)
		return
	if type=="normal":
		print(text)
		return

def filter_word(args,target):
	"""
	Filter words according to argument given
	"""
	if args.min != None:
		"""
		--min argument filter
		"""
		if args.min >= len(target):
			return 1 
	if args.max != None:
		"""
		--max argument filter
		"""
		if args.max <= len(target):
			return 1 
	if args.start != None:
		"""
		--start argument filter
		"""
		if target.lower()[:len(args.start)] != args.start:
			return 1
	if args.end != None:
		"""
		--end argument filter
		"""
		if target.lower()[-len(args.end):] != args.end:
			return 1
	if args.no_num:
		"""
		--no-num argument filter
		"""
		for v in target:
			try:
				int(v)
			except ValueError:
				pass
			else:
				return 1	
	return 0


class file_out_thread(threading.Thread):
	"""
	Start In new Thread and Append Words to file 
	"""
	def __init__(self,args,out,words=[]):
		"""
		Initial function
		"""
		threading.Thread.__init__(self)
		self.out=open(out,"a+")
		self.args=args
		self.words=words
		self.appended=0
		self.rejected=0

	def run(self,target):
		wlock.acquire()
		if self.args.check:
			"""
			Check for existing words in output file if --check argument is given.
			"""
			if target in self.words:
				"""
				Reject if target word exist in output file.
				"""
				self.rejected += 1
			else:
				self.appended +=1
				self.out.write(target)
		else:
			self.out.write(target)
			self.appended += 1
		wlock.release()

	def file_close(self):
		"""
		Close output file.
		"""
		self.out.close()

def wlist_filter(args,wordlist,word=None,newline='\n'):
	found=0
	try:
		# Try to open wordlist and quit if file not found.
		open(args.wordlist,'r')
	except FileNotFoundError:
		output_f("File not found:'"+wordlist+"'",'error')
		sys.exit()

	if not args.silent:
		output_f("Initializing "+wordlist,"progress")
	if args.verbose and args.word != None:
		output_f("Search words '"+args.word+"' and processing.","info")

	# open wordlist file and store individual lines in words variable.
	file=open(wordlist,"r",errors="ignore",encoding="utf-8")
	words=file.readlines()
	if args.sort:
		# Sord wordlist lines if --sort argument is given
		words.sort()
	if args.out != None :
		# run if --out argument is given
		if not args.silent:
			# if -s / --silent argument is not given ask user if they want to append
			# in the given file.
			# if answer in no quit program
			output_f("Append in '"+args.out+"' Y/N?",'warn')
			if input() in ["no",'n',"N","NO","not","NOT"]:
				output_f("Answer in 'NO' exiting now..","info")
				sys.exit()
		try:
			# open output file in read mode and store lines in o_file_line
			# create empty array if file not found 
			file=open(args.out,"r")
			o_file_line=file.readlines()
			file.close()
		except FileNotFoundError:
			output_f("File not found '"+args.out+"' (Creating new file).","info")
			o_file_line = []
		appended = 0
		rejected = 0
	time_a=time.time()
	if not args.silent:
		output_f('Searching',"info")
	if args.out != None:
		out_thread=file_out_thread(args,args.out,words=o_file_line)
	if args.word != None:
		word=args.word.split(",")
		for word_init in words:
			word_init=word_init[:-len(newline)]
			for search_word in word:
				if args.word != None:
					if args.no_case:
							search_word=search_word.lower()
							word_init=word_init.lower()
					if search_word in word_init:
						if filter_word(args,word_init):
							continue
						if args.out != None:
							out_thread.run(word_init+'\n')
						if args.verbose:
							output_f("Found: "+word_init,"progress")
						found+=1
	else:
		for word_init in words:
			word_init=word_init[:-len(newline)]

			if filter_word(args,word_init):
				continue
			found +=1
			if args.out != None:
				out_thread.run(word_init+'\n')

			if args.verbose:
				output_f("Found: "+word_init,"progress")
	time_b=time.time()
	if args.word != None:
		total_search=len(words)*len(word)
		output_f("Found: "+str(found)+"\t\t Total Search: "+str(total_search),"stat")
	else:
		total_search=len(words)
		output_f("Found: "+str(found)+"\t\t Total Search: "+str(total_search),"stat")
	if args.out != None:
		output_f("Appended: "+str(out_thread.appended)+"\t\t Rejected: "+str(out_thread.rejected))
	if args.verbose:
		output_f("Time Taken: "+str(round(time_b-time_a,2))+"s")
		output_f("Avrage speed: "+str(round(total_search/(time_b-time_a),2))+" search/s")	
if __name__ == '__main__':
	wlock=threading.Lock()
	args=arg_init()
	try:
		wlist_filter(args,args.wordlist)
	except KeyboardInterrupt:
		print()