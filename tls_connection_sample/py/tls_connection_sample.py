import os
import socket
import ssl
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
import shutil
import subprocess



class TLSServer:
    def __init__(self, certfile, keyfile, cid, port):
        self.certfile = certfile
        self.keyfile = keyfile
        self.cid = cid
        self.port = port
        self.server_sock = None
        self.ca_cert_data = ""

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
        server_address = (socket.VMADDR_CID_ANY, self.port)
        self.server_sock.bind(server_address)
        self.server_sock.listen(1)

        print('Server started on CID:', self.cid, 'Port:', self.port)
        print('Address:', server_address)
        print('Hostname:', socket.gethostname())

        with open(self.certfile, 'r') as ca_cert_file:
            print('Contents of ca.crt:')
            self.ca_cert_data = ca_cert_file.read()
            print(self.ca_cert_data)

        ca_cert_sent = False

        while True:
            client_sock, client_address = self.server_sock.accept()
            print('Client connected:', client_address)

            if not ca_cert_sent:
                client_sock.sendall(self.ca_cert_data.encode()) #encoded
                ca_cert_sent = True

            client_sock.close()
            break

    def start_tls(self):
        self.server_sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        server_address = (socket.VMADDR_CID_ANY, self.port)
        self.server_sock.bind(server_address)
        self.server_sock.listen(1)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile, password=None)

        while True:
            client_sock, client_address = self.server_sock.accept()
            print('CLient connected')
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
        self.ca_cert_data = ""

    def add_ca_certificate_to_trust_store(self):
        bash_script = "add_certificate.sh"  # Replace with the actual bash script file name
        subprocess.run(["sudo", "bash", bash_script], check=True)

    def write_bytes_to_file(self, data, file_path):
        try:
            with open(file_path, "wb") as file:
                file.write(data)
            print("Data successfully written to file.")
        except IOError:
            print("An error occurred while writing to the file.")

    def retrieve_ca_certificate(self):
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.connect((self.cid, self.port))
        self.ca_cert_data = b""  # Initialize as bytes
        while True:
            data = self.sock.recv(1024)
            self.ca_cert_data += data
            if not data:
                break
        self.sock.close()
        file_path = 'ca.crt'
        self.write_bytes_to_file(self.ca_cert_data, file_path)
        self.add_ca_certificate_to_trust_store()

    def connect(self):
        # self.retrieve_ca_certificate()
        # self.add_ca_certificate_to_trust_store()

        self.client_sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        server_address = (self.cid, self.port)
        self.client_sock.connect(server_address)

        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
        context.set_default_verify_paths()
        # context.load_verify_locations()

        ssl_client_sock = context.wrap_socket(self.client_sock, server_hostname=str(self.cid))
        # ssl_client_sock = context.wrap_socket(self.client_sock, server_hostname=hostname)

        print("TLS Client connected")

        data = ssl_client_sock.recv(1024)
        print('Received from server:', data.decode())
        ssl_client_sock.send(b'Hello from the client!')

        ssl_client_sock.close()
        self.client_sock.close()
