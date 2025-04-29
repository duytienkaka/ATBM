from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_key(key, filename="aes.key"):
    with open(filename, "wb") as f:
        f.write(key)

def load_key(filename="aes.key"):
    with open(filename, "rb") as f:
        return f.read()

def encrypt_message(key, message):
    return Fernet(key).encrypt(message.encode())

def decrypt_message(key, encrypted_message):
    return Fernet(key).decrypt(encrypted_message).decode()
