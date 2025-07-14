Week 1: CLI Secure File Vault

This is a simple but secure command-line file vault written in Python. It uses Fernet symmetric encryption to protect your files and supports optional deletion of originals or encrypted files with CLI flags.

Features
- Encrypt any file using symmetric key encryption
- Decrypt previously encrypted files
- Securely stores your .vault.key encryption key
- Prevents overwriting of encrypted or decrypted versions
- Optional flags to:
  - --secure delete the original after encryption
  - --cleanup delete the encrypted file after decryption

How to Use

Make sure you're in the right folder and you have a file like test.txt ready.

1. Encrypt a file
python3 vault.py test.txt encrypt

2. Decrypt a file
python3 vault.py test.encrypted.txt decrypt

With Flags (MUST be used on the same line)

Encrypt + delete original
python3 vault.py test.txt encrypt --secure

Decrypt + delete encrypted version
python3 vault.py test.encrypted.txt decrypt --cleanup

Important: Flags must be used on the same line as the encrypt/decrypt command. Running them after has no effect.

/week1_cli_vault/
├── vault.py              # Week 1 CLI encryption/decryption program
├── test.txt              # Sample file to test encryption and decryption
├── test.encrypted.txt    # Encrypted output (generated)
├── test.decrypted.txt    # Decrypted output (generated)
├── requirements.txt      # Python package dependencies
└── README.md             # Documentation for Week 1

How It Works
- When encrypting:
  - The file is encrypted and saved as yourfile.encrypted.txt
  - If --secure is passed, the original is deleted
- When decrypting:
  - The encrypted file is decrypted and saved as yourfile.decrypted.txt
  - If --cleanup is passed, the encrypted version is deleted
Future Work (Preview for Week 2+)

- Add password-based key derivation using PBKDF2
- Secure delete using overwrite tools
- Hide key file in OS-protected folders
- Add GUI
- Custom .vault file formats

Built By

Shourya Jeswani
BaSc Computer Science — McMaster University
GitHub: @sherryj23
