#!/bin/sh
echo "Flask app is ready! Starting socat..."

ip addr add 127.0.0.1/32 dev lo
ip link set dev lo up

# Replace these values with the desired port numbers you want to use
HOST_PORT=5000
DOCKER_PORT=443


# Route traffic from host port 5000 to Docker container port 80 using vsock
socat vsock-listen:$HOST_PORT,reuseaddr,fork tcp-connect:127.0.0.1:$DOCKER_PORT &

gunicorn app:app --bind 0.0.0.0:443 --workers 4

# Run the Flask app using Gunicorn (you can replace 'app:app' with your app's entry point)
#python3 app.py
