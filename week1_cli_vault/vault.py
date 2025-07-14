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
    
def encrypt(filename):
    key = load()
    fernet = Fernet(key)
    if not os.path.exists(filename):
        return("file doesnt exist")
    if os.path.exists(filename + ".encrypted"):
        return (" Encrypted file already exists. Choose a different name or delete it.")
    file = open(filename,"rb")
    orignal_file_text = file.read()
    file.close()
    cipher_text = fernet.encrypt(orignal_file_text)
    file = open(filename + ".encrypted","wb")
    file.write(cipher_text)
    file.close()
    return ("file encrypted")
    
def decrypt(filename):
    key = load()
    fernet = Fernet(key)
    if not os.path.exists(filename):
        return("encrypted file doesnt exist")
    if os.path.exists(filename + ".decrypted"):
        return ("Decrypted file already exists. Choose a different name or delete it.")
    file = open(filename,"rb")
    cipher_text = file.read()
    try:
        plain_text = fernet.decrypt(cipher_text)
    except InvalidToken:
        return ("The file is not encrypted or it was encrypted with a different key, so it cannot be decrypted")
    file = open(filename + ".decrypted","wb")
    file.write(plain_text)
    file.close()
    return ("file is now decrypted")

def main():
    parser = argparse.ArgumentParser(description="A simple CLI program that encrypts and decrypts files.")
    parser.add_argument("filename", help = "the file to encrypt or decrypt")
    parser.add_argument("command", choices=['encrypt','decrypt'],help= "enrcypt or decrypt")
    arguments = parser.parse_args()
    
    if arguments.command == "encrypt":
        result = encrypt(arguments.filename)
        print(result)
    elif arguments.command == "decrypt":
        result = decrypt(arguments.filename)
        print(result)

if __name__ == "__main__":
    main()
