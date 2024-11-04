# Caesar Cipher with Permutation Implementation

def create_permuted_alphabet(key2):
    key2 = ''.join(dict.fromkeys(key2.upper()))
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    permuted_alphabet = key2 + ''.join(letter for letter in alphabet if letter not in key2)
    return permuted_alphabet


def encrypt(message, key1, permuted_alphabet):
    cipher = ''
    for char in message:
        if char in permuted_alphabet:
            index = permuted_alphabet.index(char)
            new_index = (index + key1) % 26
            cipher += permuted_alphabet[new_index]
    return cipher


def decrypt(cipher, key1, permuted_alphabet):
    message = ''
    for char in cipher:
        if char in permuted_alphabet:
            index = permuted_alphabet.index(char)
            new_index = (index - key1) % 26
            message += permuted_alphabet[new_index]
    return message


def get_valid_key1():
    while True:
        try:
            key = int(input("Enter the first key (1-25): "))
            if 1 <= key <= 25:
                return key
            else:
                print("Key must be between 1 and 25. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 25.")


def get_valid_key2():
    while True:
        key = input("Enter the second key (at least 7 letters, A-Z only): ").upper()
        if len(key) >= 7 and key.isalpha():
            return key
        else:
            print("Invalid input. The key must be at least 7 letters long and contain only A-Z.")


def get_valid_text(prompt):
    while True:
        text = input(prompt).upper().replace(" ", "")
        if all(char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for char in text):
            return text
        else:
            print("Invalid input. Use only letters A-Z. Please try again.")


def main():
    while True:
        print("\nCaesar Cipher with Permutation")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = input("Choose operation (1/2/3): ")

        if choice == '3':
            print("Exiting program.")
            break
        elif choice in ['1', '2']:
            key1 = get_valid_key1()
            key2 = get_valid_key2()
            permuted_alphabet = create_permuted_alphabet(key2)
            print(f"Permuted alphabet: {permuted_alphabet}")

            if choice == '1':
                message = get_valid_text("Enter the message to encrypt: ")
                result = encrypt(message, key1, permuted_alphabet)
                print(f"Encrypted message: {result}")
            else:
                cipher = get_valid_text("Enter the cipher to decrypt: ")
                result = decrypt(cipher, key1, permuted_alphabet)
                print(f"Decrypted message: {result}")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
