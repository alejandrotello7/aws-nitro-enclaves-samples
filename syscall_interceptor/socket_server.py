import json
import os
import socket
import threading
import struct

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
file_descriptor = None
file_object = None

def handle_client(client_socket):
    while True:  # Keep the connection open to handle multiple requests
        buffer = b""  # Reset buffer for each request
        while True:
            part = client_socket.recv(1024)
            buffer += part
            if not part or b'\n' in part:
                break  # Exit loop if no more data or newline is found
        if not buffer:
            break  # Exit the outer loop if no data is received (client closed connection)

        try:
            # Decode buffer up to the first newline character
            data, _ = buffer.split(b'\n', 1)
            event_data = json.loads(data.decode('utf-8'))

            # Process the JSON data
            response_int = process_json_data(event_data)

            # Send the response back to the client
            response_int_network_order = socket.htonl(response_int)
            response_data = struct.pack('I', response_int_network_order)
            client_socket.sendall(response_data)


        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # Optionally send an error response back to the client

    # client_socket.close()  # Close the connection when done

def process_json_data(event_data):
    global file_object
    response_int = 0

    if event_data["operation"] == 1:
        filename = event_data["filename"]
        print(f"Received message from BPF program: {filename}")

        # Close the previously opened file
        if file_object:
            file_object.close()

        # Open the new file
        file_object = open(filename, 'w')
        response_int = file_object.fileno()
        print(f'File descriptor returned: {response_int}')

    elif event_data["operation"] == 2:
        file_descriptor = event_data["file_descriptor"]

        if file_descriptor and file_object:
            data = event_data["data"]
            print(f"Data received: {data}")
            bytes_written = os.write(file_descriptor, data.encode('utf-8'))
            response_int = bytes_written;
            print(f"Response: {response_int}")

    elif event_data["operation"] == 3:
        filename = event_data["filename"]
        print(f"File to be deleted: {filename}")
        if os.remove(filename):
            response_int = 0

    elif event_data["operation"] == 4:
        file_descriptor = event_data["file_descriptor"]


    return response_int

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
