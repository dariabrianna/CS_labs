from matplotlib import pyplot as plt


unused = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'H': 5.92, 'I': 7.31, 'N': 6.95, 'S': 6.28, 'O': 7.68, 'R': 6.02,
    'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61, 'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03,
    'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10, 'Z': 0.07
}

english_language_letters_frequency = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'H': 5.92, 'I': 7.31, 'N': 6.95, 'S': 6.28, 'O': 7.68, 'R': 6.02,
    'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61, 'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03,
    'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10, 'Z': 0.07
}


def find_frequency(text):
    """
    Find the frequency of each letter in the text.
    """
    frequency = {}
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in text:
        if char in letters:
            if char.upper() in frequency:
                frequency[char.upper()] += 1
            else:
                frequency[char.upper()] = 1
    return frequency


def plot_frequency(frequency, label):
    """
    Plot the frequency of each letter in the text.
    """
    plt.bar(frequency.keys(), frequency.values())
    plt.ylabel(label)
    plt.show()


def substitute_letters(text, original_letter, new_letter):
    """
    Update unused letters from original english alphabet.
    Substitute the original letter with the new letter in the text.
    """
    if new_letter.upper() in unused:
        del unused[new_letter.upper()]

    return text.replace(original_letter, new_letter)


def write_to_file(text, filename):
    """Using this for writing the text to a special file."""
    with open(filename, 'w') as file:
        file.write(text)


def read_from_file(filename):
    """Using this for reading the text from a special file."""
    with open(filename, 'r') as file:
        return file.read()
