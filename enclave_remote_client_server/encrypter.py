from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

# Your provided public key
public_key_pem = b"""
-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkKulhaE4swLUvAKp4CpC\nay1vFAH0d0ZyBTBsVPAcVv+o+dqmArY8lqpYtMys0+5nHX/I49sYzb1u8IoyWe5O\nu3AVZ/rZAuntevdmrfS00m4tOe5LJBg2RjKB2+BbGWHCXBmEiIKVruxZYuqmMkff\nPD+X+MJJf5A9T8piq5uDebUotK4CezQZXbT85wH8PHU6cISqwddqXJm3RUVx+tEv\n8tbWC1xq3HtMYf+vdbxKV3oVQmeXHQvbOcn4OvAwVKaEiJqmX2ctJUrbL4m1yY6o\nPHWcZPb+3p4hgpxbCa9RCA6/Q+tBc0m3QbuJaJtRG0KHEcZkZEshFTZBPq+sWGAy\nYQIDAQAB\n-----END PUBLIC KEY-----
"""

# Load the public key
public_key = serialization.load_pem_public_key(
    public_key_pem,
    backend=default_backend()
)

# Message to encrypt
message = b"hello world"

# Encrypt the message
encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Encode the encrypted message with base64 to ensure it's ASCII text
encrypted_message_hex = encrypted.hex()

print(encrypted_message_hex)
