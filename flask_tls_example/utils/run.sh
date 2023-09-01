#!/bin/sh
echo "Flask app is ready! Starting socat..."

ip addr add 127.0.0.1/32 dev lo
ip link set dev lo up

HOST_PORT=5000
DOCKER_PORT=443
REGULAR_PORT=80


# Route traffic from host port 5000/80 to Docker container port 443/80 using vsock
socat vsock-listen:$HOST_PORT,reuseaddr,fork tcp-connect:127.0.0.1:$DOCKER_PORT &
socat vsock-listen:$REGULAR_PORT,reuseaddr,fork tcp-connect:127.0.0.1:$REGULAR_PORT &


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
