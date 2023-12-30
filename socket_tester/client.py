import socket

def enclave_client(host='127.0.0.1', port=7000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'Hello, server')
        data = s.recv(1024)
        print('Received:', repr(data))

if __name__ == '__main__':
    enclave_client()
