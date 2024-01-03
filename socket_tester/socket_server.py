import json
import os
import socket
import ssl
import threading
import struct

HOST = '0.0.0.0'  # Use the appropriate host
PORT = 50051

def handle_client(ssl_sock):
    while True:
        buffer = b""
        while True:
            part = ssl_sock.recv(1024)
            buffer += part
            if not part or b'\n' in part:
                break
        if not buffer:
            break

        try:
            data, _ = buffer.split(b'\n', 1)
            event_data = json.loads(data.decode('utf-8'))
            response_int = process_json_data(event_data)
            response_int_network_order = socket.htonl(response_int)
            response_data = struct.pack('I', response_int_network_order)
            ssl_sock.sendall(response_data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")

def process_json_data(event_data):
    global file_object
    response_int = 0

    if event_data["operation"] == 1:
        filename = event_data["filename"]
        print(f"Received message from BPF program: {filename}")

        if file_object:
            file_object.close()

        file_object = open(filename, 'w')
        response_int = file_object.fileno()
        print(f'File descriptor returned: {response_int}')

    elif event_data["operation"] == 2:
        file_descriptor = event_data["file_descriptor"]

        if file_descriptor and file_object:
            data = event_data["data"]
            print(f"Data received: {data}")
            bytes_written = os.write(file_descriptor, data.encode('utf-8'))
            response_int = bytes_written
            print(f"Response: {response_int}")

    elif event_data["operation"] == 3:
        filename = event_data["filename"]
        print(f"File to be deleted: {filename}")
        if os.remove(filename):
            response_int = 0

    elif event_data["operation"] == 4:
        file_descriptor = event_data["file_descriptor"]
        # Add logic for read operation

    return response_int

def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='/home/ec2-user/dev/aws-nitro-enclaves-samples/flask_tls_example/utils/enclaves.pem', keyfile='/home/ec2-user/dev/aws-nitro-enclaves-samples/flask_tls_example/utils/enclaves.key')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        ssl_sock = context.wrap_socket(client_socket, server_side=True)
        client_handler = threading.Thread(target=handle_client, args=(ssl_sock,))
        client_handler.start()


if __name__ == "__main__":
    start_server()

    context.load_verify_locations('/home/ec2-user/dev/aws-nitro-enclaves-samples/flask_tls_example/utils/enclaves.pem')  # Path to CA certificate
