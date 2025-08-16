"""
rot13cipher.py

This module provides a function to perform ROT13 cipher encoding/decoding.
ROT13 is a Caesar cipher with a fixed shift of 13, meaning applying it
twice returns the original text.
"""

def rot13cipher(text: str) -> str:
    """
    Apply ROT13 cipher to the input text.

    Parameters:
        text (str): The input string to encode or decode.

    Returns:
        str: The transformed string after applying ROT13.
    """
    result = []

    for char in text:
        if char.islower():
            # shift lowercase letters
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif char.isupper():
            # shift uppercase letters
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        else:
            # leave non-alphabetic characters unchanged
            result.append(char)

    return "".join(result)


if __name__ == "__main__":
    sample = input("Enter text to apply ROT13: ")
    print(rot13cipher(sample))
