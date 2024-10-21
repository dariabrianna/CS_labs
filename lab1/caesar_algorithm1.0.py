# Caesar Cipher Implementation

# Define the alphabet
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def encrypt(message, key):
    cipher = ''
    for char in message:
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index + key) % 26
            cipher += alphabet[new_index]
    return cipher


def decrypt(cipher, key):
    message = ''
    for char in cipher:
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index - key) % 26
            message += alphabet[new_index]
    return message


def get_valid_key():
    while True:
        try:
            key = int(input("Enter the key (1-25): "))
            if 1 <= key <= 25:
                return key
            else:
                print("Key must be between 1 and 25.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_valid_text(prompt):
    while True:
        text = input(prompt).upper().replace(" ", "")
        if all(char in alphabet for char in text):
            return text
        else:
            print("Invalid input. Use only letters A-Z.")


def main():
    print("Caesar Cipher")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    choice = input("Choose operation (1/2/3): ")

    while choice != '3':
        if choice == '1':
            message = get_valid_text("Enter the message to encrypt: ")
            key = get_valid_key()
            cipher = encrypt(message, key)
            print(f"Encrypted message: {cipher}")
        elif choice == '2':
            cipher = get_valid_text("Enter the cipher to decrypt: ")
            key = get_valid_key()
            message = decrypt(cipher, key)
            print(f"Decrypted message: {message}")
        else:
            print("Invalid choice. Please try again.")

        print("\nCaesar Cipher")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = input("Choose operation (1/2/3): ")

    print("Exiting program.")


if __name__ == "__main__":
    main()
