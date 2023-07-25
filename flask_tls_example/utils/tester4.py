import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes


def encrypt_message(public_key_pem, message):
    public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))
    encrypted_message = public_key.encrypt(
        message.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message.hex()


if __name__ == '__main__':
    # Replace this with your pre-existing public key
    public_key_pem = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuKhGZSkHoZxUoEtK3Jxk
GX8Ze5dFFG0PlqbYq80LKi6iW1UDJLuBxWUbOZ6w6sASMvFvtEYTwv/+6k5jYFjY
OBa9fvPT0YYh8A+oco4tvx29xNLhqxIj+N0f89HtspH1PAMz2K0b8bDu2oKsjKQR
xqOh4BtZ9+gzIxUZhtFiDQiETGO/FpzKizBVvfpEJlYcfia1ZWXnj60EbxGdpJWw
vw6E0Ytc0jYgiADQNcb3R+c8pmKtEiwS4E6sjaJ4jmrv4PAMT/l5jnyXjc3a3WVz
Ko09PRSDKoRHKaH2R1g87BlXnbF/ApYSjNb4kdDO9u9lkcUiHEt1KIdTGu+iGSR5
iwIDAQAB
-----END PUBLIC KEY-----

    """

    # Example message to be encrypted
    message = "This is a secret message."

    # Encrypt the message using the public key
    encrypted_message = encrypt_message(public_key_pem, message)

    print("Encrypted Message:")
    print(encrypted_message)


# curl -X POST -F "encoded_message=808026d8ef6d7e6ce5740c9290b4bdf013acbe21b706341236faab63b375fa0f07ab9b463dc9351ce8702d21399c80f35a92f8d8c590db603b9123e8348b605ce59b6c4ee75c3dbbf1795c6ab34b42872c0615581afa72ff2991c0deb190a9b5e44120c7cd3e3a5fbb20d42921c9be3b92ea6dd9ddd9c0d9cb5a2ab3d8c6f44bcef2105e45cdd20d3c4e97278cc4d98f3ebb53bd8a63d7e38faf7d3ab80707ec93b5ee0fa32493eb6b46976cf673795d73f4008a2eed6d6b45994a2c914672eed570c87b6d02afadf6ded320dc9373b30c989c97bc76610d54f89fd521c911207569f65e70f8a4e9801887c007b6dde80ac86cfe0760d17b5272dafb2f643f2b
# " http://ec2-3-68-116-52.eu-central-1.compute.amazonaws.com:5000/api/decode
#



