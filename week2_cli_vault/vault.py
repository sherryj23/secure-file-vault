import base64
import os
import argparse
from cryptography.fernet import Fernet, InvalidToken
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from getpass import getpass
import pyotp
import qrcode
import sys
import time
def setup_totp(username):
    secret = pyotp.random_base32()
    file = open(f".vault_totp_{username}","w")
    file.write(secret)
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="FileVaultApp")
    qrcode.make(uri).show()
    print(f"TOTP secret saved for user '{username}'.")
    print("Scan the QR code in your Authenticator app.")
def get_createsalt(username):
    FILENAME = f".vault_salt_{username}"
    if os.path.exists(FILENAME):
        file = open(FILENAME, "rb")
        file_return = file.read()
        file.close()
        return file_return
    else:
        salt = os.urandom(16)
        file = open(FILENAME,"wb")
        file.write(salt)
        file.close()
        return salt
def load():
    username = input("What is your username")
    password = getpass("Enter your password")
    salt = get_createsalt(username)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations = 100000,backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    totp_file = f".vault_totp_{username}"
    try:
        file = open(totp_file,"r")
        secret = file.read()
    except FileNotFoundError:
        print(f"TOTP setup not found for user '{username}'. Run setup_totp('{username}') before trying again.")
        return None 
    totp = pyotp.TOTP(secret)
    code = input("Enter your 6-digit TOTP code: ")
    if not totp.verify(code):
        print("Invalid 2FA code. Access denied.")
        return None

    return key

def encrypt(filename,key, secure=False):
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

def decrypt(filename,key, cleanup=False):
    
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
    key = load()
    if key is None:
        print("Authentication failed. Exiting program.")
        sys.exit(1)  

    parser = argparse.ArgumentParser(description="A simple CLI program that encrypts and decrypts files.")
    parser.add_argument("filename", help="The file to encrypt or decrypt")
    parser.add_argument("command", choices=['encrypt', 'decrypt'], help="encrypt or decrypt")
    parser.add_argument("--secure", action="store_true", help="Delete original file after encrypting")
    parser.add_argument("--cleanup", action="store_true", help="Delete encrypted file after decrypting")

    arguments = parser.parse_args()

    if arguments.command == "encrypt":
        result = encrypt(arguments.filename, key, secure=arguments.secure)
        print(result)
    elif arguments.command == "decrypt":
        result = decrypt(arguments.filename, key, cleanup=arguments.cleanup)
        print(result)

if __name__ == "__main__":
    main()