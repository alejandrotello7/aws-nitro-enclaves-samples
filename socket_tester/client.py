import socket
import time

def enclave_client(host='127.0.0.1', port=7000, interval=5):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(b'Hello, server')
                data = s.recv(1024)
                print('Received:', repr(data))
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait for a specified interval before next connection attempt
        time.sleep(interval)

if __name__ == '__main__':
    enclave_client()
