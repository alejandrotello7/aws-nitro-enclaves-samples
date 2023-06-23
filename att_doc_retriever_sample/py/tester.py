from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def encode_message(message, public_key_path):
    # Load the public key from file
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    # Encode the message
    encoded_message = public_key.encrypt(
        message.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encoded_message

def decode_message(encoded_message, private_key_path):
    # Load the private key from file
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    # Decode the message
    decoded_message = private_key.decrypt(
        encoded_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decoded_message.decode("utf-8")

def write_string_to_file(string, file_path):
    try:
        with open(file_path, "w") as file:
            file.write(string)
        print("String successfully written to file.")
    except IOError:
        print("An error occurred while writing to the file.")


# Usage
public_key_path = "tester_public.pem"
private_key_path = "tester_private.pem"
message = "Hello, world!"

encoded_message = encode_message(message, public_key_path)
print(message)
print(encoded_message)

decode_messages = decode_message(encoded_message, private_key_path)
print(decode_messages)

# Usage example
text = "Hello, World!"
file_path = "output.txt"
write_string_to_file(text, file_path)