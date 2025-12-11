#! /usr/bin/python3
import argparse
import sys
import time
import datetime


def read_wordlist(wordlist_path, sort=False):
    """
    Read wordlist from file and return a list of words.
    """
    try:
        with open(wordlist_path, 'r', errors="ignore", encoding="utf-8") as f:
            words = f.readlines()
    except FileNotFoundError:
        print(f"[*] File not found:'{wordlist_path}'")
        sys.exit(1)

    if sort:
        words.sort()
    return [word.strip() for word in words]


def write_output(output_file, words, check=False, silent=False):
    """
    Write a list of words to the output file or stdout.
    """
    if not output_file:
        for word in words:
            print(word)
        return

    existing_words = set()
    if check:
        try:
            with open(output_file, 'r', errors="ignore", encoding="utf-8") as f:
                existing_words = set(line.strip() for line in f)
        except FileNotFoundError:
            pass

    appended_count = 0
    # Always open in 'a' for this function, generate_wordlist has its own writer
    with open(output_file, 'a', errors="ignore", encoding="utf-8") as f:
        for word in words:
            if check and word in existing_words:
                continue
            f.write(word + '\n')
            appended_count += 1

    if not silent:
        print(f"[+] Appended: {appended_count} words to {output_file}")

def is_word_filtered(word, min_len, max_len, start, end, no_num):
    """
    Check if a word should be filtered based on criteria.
    """
    if min_len is not None and len(word) < min_len:
        return True
    if max_len is not None and len(word) > max_len:
        return True
    if start is not None and not word.lower().startswith(start.lower()):
        return True
    if end is not None and not word.lower().endswith(end.lower()):
        return True
    if no_num and any(char.isdigit() for char in word):
        return True
    return False

def filter_wordlist(args):
    """
    Handle the 'filter' subcommand.
    """
    if not args.silent:
        print(f"[+] Initializing filter on {args.wordlist}")

    start_time = time.time()

    words = read_wordlist(args.wordlist, args.sort)
    original_word_count = len(words)

    filtered_words = []
    search_terms = args.word.split(',') if args.word else None

    for word in words:
        if search_terms:
            match = False
            for term in search_terms:
                if args.no_case:
                    if term.lower() in word.lower():
                        match = True
                        break
                else:
                    if term in word:
                        match = True
                        break
            if not match:
                continue

        if not is_word_filtered(word, args.min, args.max, args.start, args.end, args.no_num):
            filtered_words.append(word)

    # For filtering, we append by default. Let's create the file if it doesn't exist.
    if args.out:
        with open(args.out, 'a', encoding="utf-8"):
            pass
    write_output(args.out, filtered_words, args.check, args.silent)

    end_time = time.time()

    if not args.silent:
        print(f"--- Found: {len(filtered_words)} Total Search: {original_word_count} ---")
        if args.verbose:
            print(f"Time Taken: {round(end_time - start_time, 2)}s")
            if end_time - start_time > 0:
                print(f"Average speed: {round(original_word_count / (end_time - start_time), 2)} search/s")


def generate_wordlist(args):
    """
    Handle the 'generate' subcommand iteratively to save memory.
    """
    if not args.silent:
        print(f"[+] Generating wordlist from {args.input}")

    try:
        lines = read_wordlist(args.input)
        base_words = [line.split()[0] for line in lines if line.split()]

        output_stream = open(args.out, 'w', encoding='utf-8') if args.out else sys.stdout
    except Exception as e:
        print(f"[!] Error setting up generation: {e}")
        sys.exit(1)
        
    with output_stream:
        transformed_words = set(word.lower() for word in base_words)
        if args.capitalize:
            transformed_words.update([word.capitalize() for word in base_words])

        # Suffixes to add
        suffixes = []
        if args.add_numbers:
            try:
                start, end = map(int, args.add_numbers.split('-'))
                suffixes.extend(map(str, range(start, end + 1)))
            except (ValueError, IndexError):
                print("\n[!] Invalid number range format. Use START-END, e.g., '1-100'.")
                sys.exit(1)
        
        if args.add_years:
            current_year = datetime.datetime.now().year
            suffixes.extend(map(str, range(current_year - 5, current_year + 1)))

        if args.add_common_suffixes:
            suffixes.extend(['123', '12345', '@123', '!', '@', '#', '$'])

        spinner = ['/', '-', '\\', '|']
        spinner_idx = 0
        total_generated_count = 0

        # First, write the transformed base words themselves
        for word in sorted(list(transformed_words)):
            output_stream.write(word + '\n')
            total_generated_count += 1

        # Then, generate and write words with suffixes iteratively
        for word in sorted(list(transformed_words)):
            for suffix in suffixes:
                output_stream.write(word + suffix + '\n')
                total_generated_count += 1
                
                if not args.silent and total_generated_count % 1000 == 0:
                    progress_char = spinner[spinner_idx % len(spinner)]
                    sys.stdout.write(f'\r[{progress_char}] Generating... {total_generated_count} words generated.')
                    sys.stdout.flush()
                    spinner_idx += 1
    
    if not args.silent:
        sys.stdout.write('\n') # New line after spinner
        print(f"[+] Finished. Generated {total_generated_count} words.")
        if args.out:
            print(f"Wordlist saved to {args.out}")

def main():
    """
    Main function to parse arguments and run the script.
    """
    parser = argparse.ArgumentParser(
        description="A script to filter and generate wordlists.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-s", "--silent", help="Silent mode", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose mode (for filter command)", action="store_true")

    subparsers = parser.add_subparsers(dest='command', required=True, help='Sub-command help')

    # Filter command
    parser_filter = subparsers.add_parser('filter', help='Filter a wordlist')
    parser_filter.add_argument("wordlist", help="Wordlist to work with", type=str)
    parser_filter.add_argument("-w", "--word", help="Look for specific word (',' to separate words)", type=str)
    parser_filter.add_argument("-o", "--out", help="Output file")
    parser_filter.add_argument("-c", "--no-case", help="Ignore case matching", action="store_true")
    parser_filter.add_argument("--sort", help="Sort wordlist before processing", action="store_true")
    parser_filter.add_argument("--check", help="Check for duplicates in the output file before appending (slow)", action="store_true")
    parser_filter.add_argument("--min", help="Minimum length of word", type=int)
    parser_filter.add_argument("--max", help="Maximum length of word", type=int)
    parser_filter.add_argument("--start", help="Match starting of word")
    parser_filter.add_argument("--end", help="Match end of word")
    parser_filter.add_argument("--no-num", help="Ignore words containing numbers", action="store_true")
    parser_filter.set_defaults(func=filter_wordlist)

    # Generate command
    parser_generate = subparsers.add_parser('generate', help='Generate wordlist variations from a list of names.')
    parser_generate.add_argument("-i", "--input", help="Input file with names (e.g., nepali-names.txt)", default="nepali-names.txt")
    parser_generate.add_argument("-o", "--out", help="Output file for generated list")
    parser_generate.add_argument("--capitalize", help="Capitalize the first letter of names.", action="store_true")
    parser_generate.add_argument("--add-numbers", help="Append numbers to names. Use format START-END (e.g., 1-100).", type=str)
    parser_generate.add_argument("--add-years", help="Append recent years to names.", action="store_true")
    parser_generate.add_argument("--add-common-suffixes", help="Append common suffixes (e.g., 123, @123).", action="store_true")
    parser_generate.set_defaults(func=generate_wordlist)

    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n[+] KeyboardInterrupt. Exiting.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()