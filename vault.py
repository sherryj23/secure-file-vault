import os
import argparse
from cryptography.fernet import Fernet, InvalidToken
KEY_FILE = ".vault.key"
def load():
    if os.path.exists(KEY_FILE):
        file = open(KEY_FILE, "rb")
        key = file.read()
        file.close()
        return key 
    else:
        key = Fernet.generate_key()
        file = open(KEY_FILE,"wb")
        file.write(key)
        file.close()
        return key
def encrypt(filename, secure=False):
    key = load()
    fernet = Fernet(key)
    if not os.path.exists(filename):
        return("file doesnt exist")
    base, ext = os.path.splitext(filename)
    encrypted_name = base + ".encrypted" + ext
    if os.path.exists(encrypted_name):
        return ("Encrypted file already exists. Choose a different name or delete it.")

    file = open(filename, "rb")
    original_file_text = file.read()
    file.close()

    cipher_text = fernet.encrypt(original_file_text)

    file = open(encrypted_name, "wb")
    file.write(cipher_text)
    file.close()
    if secure:
        os.remove(filename)
        print("Original file securely deleted.")
    return ("file encrypted")
def decrypt(filename, cleanup=False):
    key = load()
    fernet = Fernet(key)
    if not os.path.exists(filename):
        return("encrypted file doesnt exist")
    base, ext = os.path.splitext(filename)
    decrypted_name = base.replace(".encrypted", "") + ".decrypted" + ext
    if os.path.exists(decrypted_name):
        return ("Decrypted file already exists. Choose a different name or delete it.")

    file = open(filename, "rb")
    cipher_text = file.read()
    try:
        plain_text = fernet.decrypt(cipher_text)
    except InvalidToken:
        return ("The file is not encrypted or it was encrypted with a different key, so it cannot be decrypted")

    file = open(decrypted_name, "wb")
    file.write(plain_text)
    file.close()
    
    if cleanup:
        os.remove(filename)
        print("Encrypted file deleted.")

    return ("file is now decrypted")
def main():
    parser = argparse.ArgumentParser(description="A simple CLI program that encrypts and decrypts files.")
    parser.add_argument("filename", help="the file to encrypt or decrypt")
    parser.add_argument("command", choices=['encrypt', 'decrypt'], help="encrypt or decrypt")
    parser.add_argument("--secure", action="store_true", help="Delete original file after encrypting")
    parser.add_argument("--cleanup", action="store_true", help="Delete encrypted file after decrypting")

    arguments = parser.parse_args()

    if arguments.command == "encrypt":
        result = encrypt(arguments.filename, secure=arguments.secure)
        print(result)
    elif arguments.command == "decrypt":
        result = decrypt(arguments.filename, cleanup=arguments.cleanup)
        print(result)

if __name__ == "__main__":
    main()
