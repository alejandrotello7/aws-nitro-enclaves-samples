from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Replace <ca_certificate_data> with the actual contents of the CA certificate
ca_certificate_data = """
-----BEGIN CERTIFICATE-----
MIICwDCCAaigAwIBAgIUQ9Jjvhiv45Lv0E++zwBz00crtf8wDQYJKoZIhvcNAQEL
BQAwFDESMBAGA1UEAwwJbG9jYWxob3N0MB4XDTIzMDYzMDAzNTIzMFoXDTI0MDYy
OTAzNTIzMFowDTELMAkGA1UEAwwCMTYwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw
ggEKAoIBAQCBvb5BLR3cfhyOhJbiai8LfJY3pxUaSBQOZH5btPbV6+vBKDrzWg0Q
q5MDz/vwfy2PlMk007X3eGB3J7FslBmb0++DvdGfu6S5/r9ZyPdnG6oVADh+m1Jh
BipuuBaiiHgFvhvQRjkvmJOfADHwCNSRa/cObdtO9OeZHWTdUncWn9pE2XIufrxK
3OojESLNO3j7otgo4fOis9aybKiAMFcVgs87K2ojjefJKXQhmBuf/Zbm2ZbYUsxF
mkFpnJBx0mDSf6Q5LQPcF6ahb24TE1CqyLxOhTF+O95ceDiV9Bte392ayTfiv+ct
LpuksoGqdQwvWuAa1sF+gKQE2/rFULu/AgMBAAGjETAPMA0GA1UdEQQGMASCAjE2
MA0GCSqGSIb3DQEBCwUAA4IBAQCAh9JZFFIoGCBIMOOZ8sk8jYI72sZ9//2H2fVO
nJ3a7JvecGjDRHfY0+NT/496ZXLhXqEZv5wtC5HjHaHvfzED2OQ24eG52c1xlaCP
O/u1fKp3ln6iA1dFazJwdOQWo7Zy2jICBO/deL0a5QenAs8QXu9VDnh3XyU2bTzK
hF9SXY2a8BRRmZu0/osiXP2UyQqhN6IygBb5fqD0+y0I5mvfKwfOCVu5JAI+CN+P
VXmPnX7T2fYdp3V/zvUV0dRkaphKrRGf8KrW9KPPCHIMR2QtFPVjNc8W9NLUAhqT
MuL9a+g+yGTPdJPTC/md4BzC3IldFPQi4NN7/VINIXAMsSIk
-----END CERTIFICATE-----
"""

# Load the CA certificate
ca_certificate = x509.load_pem_x509_certificate(ca_certificate_data.encode(), default_backend())

# Extract the public key
public_key = ca_certificate.public_key()

# Serialize the public key to PEM format
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(public_key_pem.decode())