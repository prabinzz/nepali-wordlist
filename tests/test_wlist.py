import pytest
from wlist import (
    is_word_filtered,
    read_wordlist,
    write_output,
    filter_wordlist
)
import argparse
import os

def test_is_word_filtered():
    # Test min length
    assert is_word_filtered("word", min_len=5, max_len=None, start=None, end=None, no_num=False)
    assert not is_word_filtered("longerword", min_len=5, max_len=None, start=None, end=None, no_num=False)

    # Test max length
    assert is_word_filtered("toolongword", min_len=None, max_len=5, start=None, end=None, no_num=False)
    assert not is_word_filtered("word", min_len=None, max_len=5, start=None, end=None, no_num=False)

    # Test startswith
    assert not is_word_filtered("startword", min_len=None, max_len=None, start="start", end=None, no_num=False)
    assert is_word_filtered("anotherword", min_len=None, max_len=None, start="start", end=None, no_num=False)

    # Test endswith
    assert not is_word_filtered("wordend", min_len=None, max_len=None, start=None, end="end", no_num=False)
    assert is_word_filtered("anotherword", min_len=None, max_len=None, start=None, end="end", no_num=False)

    # Test no numbers
    assert is_word_filtered("wordwith1number", min_len=None, max_len=None, start=None, end=None, no_num=True)
    assert not is_word_filtered("wordwithoutnumber", min_len=None, max_len=None, start=None, end=None, no_num=True)

def test_read_wordlist(tmp_path):
    wordlist_content = "word1\nword2\nword3\n"
    wordlist_path = tmp_path / "wordlist.txt"
    wordlist_path.write_text(wordlist_content)

    words = read_wordlist(str(wordlist_path), sort=False)
    assert words == ["word1", "word2", "word3"]

    words_sorted = read_wordlist(str(wordlist_path), sort=True)
    assert words_sorted == ["word1", "word2", "word3"]

def test_write_output(tmp_path):
    words = ["word1", "word2", "word3"]
    output_path = tmp_path / "output.txt"

    # Test writing to a new file
    write_output(str(output_path), words)
    with open(output_path, "r") as f:
        content = f.read()
    assert "word1\nword2\nword3\n" in content

    # Test appending to an existing file with --check
    write_output(str(output_path), ["word3", "word4"], check=True)
    with open(output_path, "r") as f:
        content = f.read()
    assert content.count("word3") == 1
    assert "word4" in content

def test_filter_wordlist_integration(tmp_path):
    wordlist_content = "apple\nbanana\norange\ngrape1\n"
    wordlist_path = tmp_path / "wordlist.txt"
    wordlist_path.write_text(wordlist_content)
    output_path = tmp_path / "output.txt"

    # This is a bit of a hack to simulate the args object
    # that would be created by argparse
    class Args:
        def __init__(self, wordlist, out, min, no_num, word, no_case, sort, check, max, start, end, silent, verbose):
            self.wordlist = wordlist
            self.out = out
            self.min = min
            self.no_num = no_num
            self.word = word
            self.no_case = no_case
            self.sort = sort
            self.check = check
            self.max = max
            self.start = start
            self.end = end
            self.silent = silent
            self.verbose = verbose
    
    args = Args(
        wordlist=str(wordlist_path),
        out=str(output_path),
        min=6,
        no_num=True,
        word=None,
        no_case=False,
        sort=False,
        check=False,
        max=None,
        start=None,
        end=None,
        silent=True,
        verbose=False
    )
    
    filter_wordlist(args)

    with open(output_path, "r") as f:
        result = f.read().strip().split('\n')

    assert result == ["banana", "orange"]