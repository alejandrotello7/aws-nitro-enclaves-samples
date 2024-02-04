from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

# Your provided public key
public_key_pem = b"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyYV/LbxWgZw1zyj6vDAh
N5CnDyPjD4fmBe+uS0/a1I6Jgq53a7saJ7GExlr+vZe0YEP4wZc4zZP6NfSybS9M
5HuY2SuuiUjEBZ5KupRwijkJ6e+WPglpzeb1PZW6gDtQoFGd9RuNSkECu/kuiTtI
SbNxrK516k0DjKQPWgnbyESzV5ab52KWuHWZG6OXkPqdDRCG1sKFLE9yzr1cgq1T
zbtw55QfLC3DnFlSQyD0BDWYBRZ1O1CWhjBrI4aJc8s81S9QUFY3kB9O58yYqzs/
4C/FXu7JtfFKSJkbb0CjllDNF1K/LrVpxFU2LHtGJLGphQen8d5tswvyuenqSZI7
UQIDAQAB
-----END PUBLIC KEY-----
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
encrypted_message = base64.b64encode(encrypted)

print(encrypted_message.decode('ascii'))
