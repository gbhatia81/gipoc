import re


def merge_hyphenated_words(text: str) -> str:
    """
    The provided Python function merge_hyphenated_words takes a text string as input and uses the re.sub function from the re (regular expression) module to merge hyphenated words that are split across two lines by removing the hyphen and the newline character. Here's an explanation of what this code does:

    re.sub(pattern, replacement, string) is a method that searches for occurrences of the pattern in the string and replaces them with the replacement.

    The regular expression pattern r"(\w)-\n(\w)" is used as the pattern to search for:

    (\w): This is a capturing group (\w) that matches a word character (alphanumeric character or underscore) and captures it. The parentheses ( ) create a capturing group to remember this character.
    -: This matches a hyphen character.
    \n: This matches a newline character.
    (\w): This is another capturing group that matches and captures a word character.
    The replacement string r"\1\2" is used:

    \1: This refers to the first capturing group, which is the word character before the hyphen.
    \2: This refers to the second capturing group, which is the word character after the hyphen.
    """
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def fix_newlines(text: str) -> str:
    """
    The provided Python function fix_newlines takes a text string as input and uses the re.sub function from the re (regular expression) module to
    replace certain newline characters with spaces. Here's an explanation of what this code does:

    re.sub(pattern, replacement, string) is a method that searches for occurrences of the pattern in the string and replaces them with the replacement.

    The regular expression pattern r"(?<!\n)\n(?!\n)" is used as the pattern to search for. Let's break it down:

    (?<!\n): This is a negative lookbehind assertion. It means that the pattern should match a newline character (\n) only if it is not preceded by another newline character.
    In other words, it matches a newline character that is not immediately preceded by another newline character.\n: This is the actual newline character that we want to match.
    (?!\n): This is a negative lookahead assertion. It means that the pattern should match a newline character (\n) only if it is not followed by another newline character.
    In other words, it matches a newline character that is not immediately followed by another newline character.The replacement string " " is a single space character.
    """
    return re.sub(r"(?<!\n)\n(?!\n)", " ", text)


def remove_multiple_newlines(text: str) -> str:
    """_summary_
    The provided Python function remove_multiple_newlines takes a text string as input and uses the re.sub function from the re (regular expression)
    module to remove consecutive sequences of two or more newline characters (\n) and replaces them with a single newline character. Here's an explanation of what this code does:

    re.sub(pattern, replacement, string) is a method that searches for occurrences of the pattern in the string and replaces them with the replacement.

    The regular expression pattern r"\n{2,}" is used as the pattern to search for:

    \n: This matches a single newline character.
    {2,}: This quantifier specifies that the preceding \n should appear at least 2 times consecutively.
    The replacement string "\n" is a single newline character.

    So, the re.sub function effectively finds sequences of two or more consecutive newline characters in the
    input text and replaces them with a single newline character. This operation removes extra blank lines and condenses multiple consecutive blank lines into a single blank line.
    """
    return re.sub(r"\n{2,}", "\n", text)
