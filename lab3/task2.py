def clean_message(message):
    allowed_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cleaned = ''.join([char for char in message.upper() if char in allowed_chars])
    return cleaned

def validate_key(key):
    if len(key) < 7:
        raise ValueError("Cheia trebuie să conțină cel puțin 7 caractere.")
    return clean_message(key)

def generate_full_key(message, key):
    key = validate_key(key)
    key_repeated = key * (len(message) // len(key)) + key[:len(message) % len(key)]
    return key_repeated

def encrypt_vigenere(message, key):
    cleaned_message = clean_message(message)
    full_key = generate_full_key(cleaned_message, key)
    encrypted = ''
    for m_char, k_char in zip(cleaned_message, full_key):
        encrypted_char_index = (ord(m_char) - ord('A') + ord(k_char) - ord('A')) % 31
        encrypted += chr(encrypted_char_index + ord('A'))
    return encrypted

def decrypt_vigenere(ciphertext, key):
    full_key = generate_full_key(ciphertext, key)
    decrypted = ''
    for c_char, k_char in zip(ciphertext, full_key):
        decrypted_char_index = (ord(c_char) - ord('A') - (ord(k_char) - ord('A'))) % 31
        decrypted += chr(decrypted_char_index + ord('A'))
    return decrypted

def main():
    try:
        operation = input("Alege operația (criptare/decriptare): ").strip().lower()
        if operation not in ['criptare', 'decriptare']:
            print("Operație invalidă. Alege între 'criptare' sau 'decriptare'.")
            return

        message = input("Introdu mesajul/criptograma: ").strip()
        key = input("Introdu cheia (cel puțin 7 caractere): ").strip()

        if operation == 'criptare':
            encrypted_message = encrypt_vigenere(message, key)
            print(f"Criptograma: {encrypted_message}")
        elif operation == 'decriptare':
            decrypted_message = decrypt_vigenere(message, key)
            print(f"Mesajul decriptat: {decrypted_message}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
