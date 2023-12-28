import socket

def socket_server():
    host = '0.0.0.0'
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)

    print(f"Listening as {host}:{port}...")

    conn, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received from client: {data}")
        data = f"Echo: {data}"
        conn.send(data.encode())

    conn.close()

if __name__ == '__main__':
    socket_server()
