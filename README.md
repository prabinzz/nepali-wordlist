# Wordlist Toolkit

[![CI](https://github.com/prabinparajuli/nepali-wordlist/actions/workflows/python-app.yml/badge.svg)](https://github.com/prabinparajuli/nepali-wordlist/actions/workflows/python-app.yml)

A versatile command-line tool for generating and manipulating wordlists. Built with performance and flexibility in mind, this tool makes it easy to create custom wordlists from a base set of names or filter existing lists to meet specific criteria.

## Key Features

-   **Advanced Wordlist Generation:** Create complex wordlists by combining base names with numbers, years, and common suffixes.
-   **Powerful Filtering:** Systematically reduce large wordlists based on length, content, character patterns, and more.
-   **Memory Efficient:** Processes large files iteratively, ensuring low and stable memory usage even with massive wordlists.
-   **Flexible Output:** Print to standard output or save results to a file.
-   **Simple & Fast:** A lightweight, dependency-free Python script that's easy to use and modify.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/prabinparajuli/nepali-wordlist.git
    cd nepali-wordlist
    ```
2.  **Set up a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The script provides two main commands: `generate` and `filter`.

---

### `generate`: Create Wordlists

This command builds a new wordlist by generating variations from a list of base names.

**Command:**
```bash
python3 wlist.py generate [OPTIONS]
```

**Options:**

| Flag                    | Description                                                 |
| ----------------------- | ----------------------------------------------------------- |
| `-i, --input <file>`    | Input file with base names (default: `nepali-names.txt`).   |
| `-o, --out <file>`      | Output file to save the wordlist.                           |
| `--capitalize`          | Capitalize the first letter of each base name.              |
| `--add-numbers <START-END>` | Append numbers in a given range (e.g., `1-1000`).         |
| `--add-years`           | Append recent years to each name.                           |
| `--add-common-suffixes` | Append common suffixes like `123`, `@`, `!`.                |

**Example:**
*Generate a wordlist from `names.txt` with capitalized variations that also end with numbers from 1 to 100.*
```bash
python3 wlist.py generate -i names.txt --capitalize --add-numbers 1-100 --out custom-list.txt
```

---

### `filter`: Filter Wordlists

This command filters a large wordlist based on a set of rules, helping you trim it down to your exact needs.

**Command:**
```bash
python3 wlist.py filter <wordlist> [OPTIONS]
```

**Options:**

| Flag                | Description                                                          |
| ------------------- | -------------------------------------------------------------------- |
| `<wordlist>`        | The path to the wordlist file to filter.                             |
| `-w, --word <term>` | Filter for lines containing a specific word or comma-separated words.|
| `-o, --out <file>`  | Output file to save the filtered list.                               |
| `--min <length>`    | Set a minimum word length.                                           |
| `--max <length>`    | Set a maximum word length.                                           |
| `--start <str>`     | Filter for words starting with a specific string.                    |
| `--end <str>`       | Filter for words ending with a specific string.                      |
| `--no-num`          | Exclude words that contain any numbers.                              |
| `--no-case`         | Perform case-insensitive matching.                                   |
| `--check`           | Prevent duplicate words from being appended to the output file (slower). |


**Example:**
*From a large wordlist `big-list.txt`, create a new list containing only words that are between 8 and 12 characters long and start with "pass".*
```bash
python3 wlist.py filter big-list.txt --min 8 --max 12 --start "pass" --out filtered.txt
```

## Contributing

Pull requests are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is provided for educational and ethical research purposes only. Ensure you have proper authorization before using it in any security testing or on any network. The user is responsible for their own actions.