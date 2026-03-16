import json
import os
import hashlib
from cryptography.fernet import Fernet

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "passwords.json")
KEY_FILE = os.path.join(SCRIPT_DIR, "secret.key")
MASTER_FILE = os.path.join(SCRIPT_DIR, "master.hash")


# -----------------------------------
# Generate or Load Encryption Key
# -----------------------------------
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()

    return Fernet(key)


# -----------------------------------
# Setup Master Password
# -----------------------------------

def setup_master():
    if not os.path.exists(MASTER_FILE):
        print("First time setup")

        master_password = input("Create master password: ")

        hashed = hashlib.sha256(master_password.encode()).hexdigest()

        with open(MASTER_FILE, "w") as f:
            f.write(hashed)

        print("Master password created")


# -----------------------------------
# Verify Master Password
# -----------------------------------
def verify_master():
    password = input("Enter master password: ")

    hashed = hashlib.sha256(password.encode()).hexdigest()

    with open(MASTER_FILE) as f:
        stored_hash = f.read()

    if hashed != stored_hash:
        print("Incorrect password")
        exit()

    print("Access granted")


# -----------------------------------
# Load Password Database
# -----------------------------------
def load_passwords():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:
        return json.load(f)


# -----------------------------------
# Save Password Database
# -----------------------------------
def save_passwords(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------
# Add Password
# -----------------------------------

def add_password(fernet):
    site = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    encrypted_password = fernet.encrypt(password.encode()).decode()

    data = load_passwords()

    data[site] = {
        "username": username,
        "password": encrypted_password
    }

    save_passwords(data)

    print("Password saved")


# -----------------------------------
# Retrieve Password
# -----------------------------------
def get_password(fernet):
    site = input("Website name: ")

    data = load_passwords()

    if site not in data:
        print("No password stored for this site")
        return

    encrypted = data[site]["password"]

    decrypted = fernet.decrypt(encrypted.encode()).decode()

    print("Username:", data[site]["username"])
    print("Password:", decrypted)


# -----------------------------------
# View All Stored Websites
# -----------------------------------
def view_sites():
    data = load_passwords()

    if not data:
        print("No saved passwords")
        return

    print("\nSaved Websites:")

    for site in data:
        print("-", site)


# -----------------------------------
# Main Program
# -----------------------------------
def main():

    setup_master()
    verify_master()

    fernet = load_key()

    while True:

        print("\nPassword Manager")
        print("1. Add password")
        print("2. Get password")
        print("3. View saved sites")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_password(fernet)

        elif choice == "2":
            get_password(fernet)

        elif choice == "3":
            view_sites()

        elif choice == "4":
            print("Goodbye")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
