import pytest
from wlist import generate_wordlist
import os
import datetime

@pytest.fixture
def setup_test_files(tmp_path):
    names_content = "test\napple"
    names_path = tmp_path / "names.txt"
    names_path.write_text(names_content, encoding="utf-8")
    
    output_path = tmp_path / "output.txt"
    
    return names_path, output_path

class Args:
    def __init__(self, input, out, capitalize=False, add_numbers=None, add_years=False, add_common_suffixes=False, silent=True):
        self.input = input
        self.out = out
        self.capitalize = capitalize
        self.add_numbers = add_numbers
        self.add_years = add_years
        self.add_common_suffixes = add_common_suffixes
        self.silent = silent

def test_generate_simple(setup_test_files):
    names_path, output_path = setup_test_files
    args = Args(input=str(names_path), out=str(output_path))
    generate_wordlist(args)
    with open(output_path, 'r', encoding="utf-8") as f:
        content = sorted([line.strip() for line in f.readlines()])
    assert content == ['apple', 'test']

def test_generate_capitalize(setup_test_files):
    names_path, output_path = setup_test_files
    args = Args(input=str(names_path), out=str(output_path), capitalize=True)
    generate_wordlist(args)
    with open(output_path, 'r', encoding="utf-8") as f:
        content = sorted([line.strip() for line in f.readlines()])
    assert content == ['Apple', 'Test', 'apple', 'test']

def test_generate_add_numbers(setup_test_files):
    names_path, output_path = setup_test_files
    args = Args(input=str(names_path), out=str(output_path), add_numbers="1-2")
    generate_wordlist(args)
    with open(output_path, 'r', encoding="utf-8") as f:
        content = sorted([line.strip() for line in f.readlines()])
    # Base words are included, plus variations
    assert sorted(content) == sorted(['apple', 'test', 'apple1', 'apple2', 'test1', 'test2'])


def test_generate_add_years(setup_test_files):
    names_path, output_path = setup_test_files
    args = Args(input=str(names_path), out=str(output_path), add_years=True)
    generate_wordlist(args)
    
    current_year = datetime.datetime.now().year
    years = [str(y) for y in range(current_year - 5, current_year + 1)]
    
    expected = {'apple', 'test'}
    for year in years:
        expected.add('apple' + year)
        expected.add('test' + year)
        
    with open(output_path, 'r', encoding="utf-8") as f:
        content = set(line.strip() for line in f.readlines())
        
    assert content == expected

def test_generate_add_common_suffixes(setup_test_files):
    names_path, output_path = setup_test_files
    args = Args(input=str(names_path), out=str(output_path), add_common_suffixes=True)
    generate_wordlist(args)
    
    suffixes = ['123', '12345', '@123', '!', '@', '#', '$']
    expected = {'apple', 'test'}
    for suffix in suffixes:
        expected.add('apple' + suffix)
        expected.add('test' + suffix)
        
    with open(output_path, 'r', encoding="utf-8") as f:
        content = set(line.strip() for line in f.readlines())
        
    assert content == expected

def test_generate_combination(setup_test_files):
    names_path, output_path = setup_test_files
    args = Args(input=str(names_path), out=str(output_path), capitalize=True, add_numbers="9-10")
    generate_wordlist(args)
    
    with open(output_path, 'r', encoding="utf-8") as f:
        content = set(line.strip() for line in f.readlines())

    expected = {
        'apple', 'test', 'Apple', 'Test',
        'apple9', 'apple10', 'test9', 'test10',
        'Apple9', 'Apple10', 'Test9', 'Test10'
    }
    
    assert content == expected