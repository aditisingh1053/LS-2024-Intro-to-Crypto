import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Generate a 16-byte salt
salt = secrets.token_bytes(16)
print("Generated Salt (Secret Key):", salt.hex())

# Define a password (this can be any byte string, and should be kept secret)
password = b'spice'

# Derive a 32-byte key from the salt using PBKDF2HMAC
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=8,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
secret_key = kdf.derive(password)
print("Derived Secret Key:", secret_key.hex())
