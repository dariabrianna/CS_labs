import re
import numpy as np
import math

def clean_key(key):
    # Eliminate duplicate letters and keep only alphabetical characters
    key = ''.join(sorted(set(key), key=key.index))
    key = re.sub(r'[^A-Za-zĂÂÎȘȚ]', '', key)
    return key.upper()

def create_playfair_matrix(key):
    alphabet = 'AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ'
    key = clean_key(key)
    matrix = []
    used_chars = set()

    # Add key letters to the matrix
    for char in key:
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)

    # Add remaining letters of the alphabet
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)

    # Calculate dimensions for the matrix based on the number of characters
    n = len(matrix)
    rows = int(math.ceil(math.sqrt(n)))
    cols = rows

    # Padding with a placeholder character if necessary
    while len(matrix) < rows * cols:
        matrix.append('X')  # Padding with 'X' or another placeholder

    return np.array(matrix).reshape(rows, cols)

# The rest of the code remains the same



def preprocess_text(text):
    # Remove any character that’s not in the Romanian alphabet
    text = re.sub(r'[^A-Za-zĂÂÎȘȚ]', '', text)
    return text.upper()


def find_position(matrix, char):
    position = np.where(matrix == char)
    return position[0][0], position[1][0]

def playfair_encrypt(matrix, plaintext):
    plaintext = preprocess_text(plaintext)
    if len(plaintext) % 2 != 0:
        plaintext += 'X'  # Padding with 'X' if odd length

    ciphertext = ''
    for i in range(0, len(plaintext), 2):
        char1, char2 = plaintext[i], plaintext[i + 1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:
            # Same row: move right
            ciphertext += matrix[row1, (col1 + 1) % 6]
            ciphertext += matrix[row2, (col2 + 1) % 6]
        elif col1 == col2:
            # Same column: move down
            ciphertext += matrix[(row1 + 1) % 6, col1]
            ciphertext += matrix[(row2 + 1) % 6, col2]
        else:
            # Rectangle: swap columns
            ciphertext += matrix[row1, col2]
            ciphertext += matrix[row2, col1]
    
    return ciphertext

def playfair_decrypt(matrix, ciphertext):
    ciphertext = preprocess_text(ciphertext)  # Ensure text is preprocessed
    plaintext = ''

    for i in range(0, len(ciphertext), 2):
        char1, char2 = ciphertext[i], ciphertext[i + 1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:
            # Same row: move left
            plaintext += matrix[row1, (col1 - 1) % 6]
            plaintext += matrix[row2, (col2 - 1) % 6]
        elif col1 == col2:
            # Same column: move up
            plaintext += matrix[(row1 - 1) % 6, col1]
            plaintext += matrix[(row2 - 1) % 6, col2]
        else:
            # Rectangle: swap columns
            plaintext += matrix[row1, col2]
            plaintext += matrix[row2, col1]

    # Remove padding 'X' if it was added
    if plaintext.endswith('X'):
        plaintext = plaintext[:-1]

    return plaintext



def main():
    operation = input("Select operation (encrypt/decrypt): ").strip().lower()
    key = input("Enter key (minimum 7 characters): ")
    while len(key) < 7:
        print("Key must be at least 7 characters long.")
        key = input("Enter key (minimum 7 characters): ")
    
    message = input("Enter message: ")
    key_matrix = create_playfair_matrix(key)
    
    if operation == 'encrypt':
        result = playfair_encrypt(key_matrix, message)
        print(f"Encrypted message: {result}")
    elif operation == 'decrypt':
        result = playfair_decrypt(key_matrix, message)
        print(f"Decrypted message: {result}")
    else:
        print("Invalid operation. Please choose 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()
