#!/bin/sh
echo "Flask app is ready! Starting socat..."
openssl version

ip addr add 127.0.0.1/32 dev lo
ip link set dev lo up

HOST_PORT=5000
DOCKER_PORT=443
REGULAR_PORT=80


LD_LIBRARY_PATH=syscall_intercept/ LD_PRELOAD=syscall_intercept/examples/example_open.so ./syscall_intercept/examples/my_program

# Route traffic from host port 5000/80 to Docker container port 443/80 using vsock
socat vsock-listen:$HOST_PORT,reuseaddr,fork tcp-connect:127.0.0.1:$DOCKER_PORT &
socat vsock-listen:$REGULAR_PORT,reuseaddr,fork tcp-connect:127.0.0.1:$REGULAR_PORT &
socat tcp-listen:7000,reuseaddr,fork vsock-connect:2:6000 &


#python3 grpc_server.py
#sleep 10

nginx -v
pip show cryptography


# Start Gunicorn in the background
gunicorn app:app --bind 0.0.0.0:8000 --workers 4 &

# Wait for a short period to allow Gunicorn to start fully (adjust the sleep duration as needed)
sleep 10

#python3 grpc_server.py &
#sleep 10

# Start Nginx in the foreground
nginx -g "daemon off;"
