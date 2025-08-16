def ceasercipher(text: str, shift: int) -> str:
    """
    Apply Caesar cipher to a given text with a given shift.
    
    Args:
        text (str): The input text to encrypt/decrypt.
        shift (int): The shift amount (can be positive or negative).
        
    Returns:
        str: The shifted text.
    """
    while shift < 0:
        shift += 26
    shift = shift % 26
    result = []

    for char in text:
        if char.islower():
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        elif char.isupper():
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            # leave non-alphabetic characters unchanged
            result.append(char)

    return "".join(result)


if __name__ == "__main__":
    name = input("Enter text: ")
    n = int(input("Enter shift: "))
    print(ceasercipher(name, n))
