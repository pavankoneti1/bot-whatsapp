import os
import base64
import secrets

def generate_key():
    key = secrets.token_bytes(16)  # 256 bits key
    return base64.urlsafe_b64encode(key).decode('utf-8')

def generate_iv():
    iv = os.urandom(16)  # 128 bits IV
    return base64.urlsafe_b64encode(iv).decode('utf-8')

# Example usage
encryption_key = generate_key()
encryption_iv = generate_iv()

print(encryption_key)
print(encryption_iv)
