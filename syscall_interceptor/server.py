import socket

def run_server(port=6000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen()
        print(f"Server listening on port {port}...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                sent_message = b"Hello from Server"
                print(f"Received:{data}")
                if not data:
                    print("not yet")
                conn.sendall(sent_message)  # Echoes back received data

if __name__ == "__main__":
    run_server()
