import socket

def start_server(port=50051):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to client at {client_address}")
        message = client_socket.recv(1024).decode()
        print(f"Received message: {message}")
        client_socket.send(f"Echo: {message}".encode())
        client_socket.close()

if __name__ == "__main__":
    start_server()
