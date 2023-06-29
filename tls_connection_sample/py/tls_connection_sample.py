import socket
import ssl
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes


class TLSServer:
    def __init__(self, certfile, keyfile, cid, port):
        self.certfile = certfile
        self.keyfile = keyfile
        self.cid = cid
        self.port = port
        self.server_sock = None

    def generate_certificate(self, common_name):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([
            x509.NameAttribute(x509.NameOID.COMMON_NAME, common_name)
        ]))
        builder = builder.issuer_name(x509.Name([
            x509.NameAttribute(x509.NameOID.COMMON_NAME, 'localhost')
        ]))
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.not_valid_before(datetime.datetime.utcnow())
        builder = builder.not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        )
        builder = builder.public_key(public_key)
        builder = builder.add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(common_name)
            ]),
            critical=False
        )
        certificate = builder.sign(
            private_key=private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend()
        )

        with open(self.certfile, 'wb') as cert_file:
            cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))
        with open(self.keyfile, 'wb') as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))


def start(self):
    common_name = str(self.cid)  # Use the client ID as the common name
    self.generate_certificate(common_name)

    self.server_sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    self.server_sock.bind((self.cid, 0))  # Bind to the CID, port 0
    self.server_sock.listen(1)

    self.port = self.server_sock.getsockname()[1]  # Update the port to the dynamically assigned port

    print('Server started on CID:', self.cid, 'Port:', self.port)

    while True:
        client_sock, client_address = self.server_sock.accept()
        print('Client connected:', client_address)

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        ssl_client_sock = context.wrap_socket(client_sock, server_side=True)

        data = ssl_client_sock.recv(1024)
        print('Received from client:', data.decode())
        ssl_client_sock.send(b'Hello from the server!')

        ssl_client_sock.close()
        client_sock.close()




class TLSClient:
    def __init__(self, cid, port, ca_certfile):
        self.cid = cid
        self.port = port
        self.ca_certfile = ca_certfile
        self.client_sock = None

    def retrieve_ca_certificate(self):
        ca_cert_file = open('ca.crt', 'wb')
        server_address = str(self.cid) + ':' + str(self.port)
        ca_cert_file.write(ssl.get_server_certificate(server_address).encode())
        ca_cert_file.close()

    def connect(self):
        self.retrieve_ca_certificate()

        self.client_sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        server_address = (socket.AF_VSOCK, self.cid, self.port)
        self.client_sock.connect(server_address)

        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(cafile=self.ca_certfile)
        ssl_client_sock = context.wrap_socket(self.client_sock, server_hostname=str(self.cid))

        print("Client connected")

        data = ssl_client_sock.recv(1024)
        print('Received from server:', data.decode())
        ssl_client_sock.send(b'Hello from the client!')

        ssl_client_sock.close()
        self.client_sock.close()
