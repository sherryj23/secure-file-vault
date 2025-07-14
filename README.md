A multi-stage file encryption project built in Python. Each week adds new features — from a secure CLI vault to a GUI-powered encryption app with password-based key derivation and cleanup flags.

Project Structure 

/secure-file-vault/
├── week1_cli_vault/         # CLI vault with Fernet encryption and file-safety flags
├── week2_security_upgrade/  # Adds PBKDF2 master password + GUI + secure deletion
└──  week3_polish/            # Final polish: cleanup, UX, and optional add-ons

Quickstart (Week 1 Example)

cd week1_cli_vault
python3 vault.py test.txt encrypt --secure
python3 vault.py test.encrypted.txt decrypt --cleanup

Setup

Install dependencies for each week as needed:
pip install -r week1_cli_vault/requirements.txt

Weekly Breakdown

Week 1: CLI Vault with Fernet Encryption
- Uses cryptography.fernet for symmetric encryption
- Auto-generates and stores a .vault.key
- Flags:
  --secure to delete the original after encryption
  --cleanup to delete the encrypted file after decryption
- CLI usage via argparse

Week 2: Security Upgrade + GUI
- PBKDF2-based key derivation
  - cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC
  - Password → derived key using salt (auto-saved/reused)
- Master password prompt
  - Secure CLI input via getpass
- GUI support
  - Tkinter drag-and-drop app
  - Integrated backend encryption/decryption
- Secure deletion
  - Auto-deletes sensitive files after action
  - Optional: use secure wipe tools (e.g. shred, srm)

Week 3: Polish & UX Improvements
- Refactor codebase for readability and modularity
- Enhanced user feedback and error messages
- Unified encryption format

Each week's folder has its own README.md with testing instructions.
"""

Built By

Shourya Jeswani
BaSc Computer Science — McMaster University
GitHub: @sherryj23
