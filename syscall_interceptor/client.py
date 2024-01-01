import socket

def connect_to_server(host="18.197.195.160", port=50051):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    message = "Hello, Server!"
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    print(f"Received from server: {response}")
    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
