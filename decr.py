from cryptography.fernet import Fernet
import bcrypt
import getpass

# Generate and load encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

# Encrypt and decrypt functions
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# User database and role-based access control
users_db = {
    "admin": {
        "password": bcrypt.hashpw(b"adminpass", bcrypt.gensalt()),
        "role": "admin"
    },
    "user": {
        "password": bcrypt.hashpw(b"userpass", bcrypt.gensalt()),
        "role": "user"
    }
}

def authenticate(username, password):
    if username in users_db and bcrypt.checkpw(password.encode(), users_db[username]['password']):
        return True
    return False

def has_access(username, resource):
    if username in users_db:
        role = users_db[username]["role"]
        if resource == "confidential_data" and role == "admin":
            return True
        elif resource == "general_data":
            return True
    return False

# Main function
def main():
    generate_key()
    key = load_key()

    print("Welcome to the Secure System")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    if authenticate(username, password):
        print(f"Hello, {username}! You are authenticated.")
        
        # Access control
        resource = input("Enter the resource you want to access (confidential_data/general_data): ")
        if has_access(username, resource):
            print(f"Access granted to {resource}.")
            
            # Encrypt and decrypt data
            message = input("Enter a message to encrypt: ")
            encrypted_message = encrypt_message(message, key)
            print(f"Encrypted message: {encrypted_message}")

            decrypted_message = decrypt_message(encrypted_message, key)
            print(f"Decrypted message: {decrypted_message}")
        else:
            print("Access denied. You do not have the necessary permissions.")
    else:
        print("Authentication failed. Incorrect username or password.")

if __name__ == "__main__":
    main()
