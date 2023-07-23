#!/bin/sh

# Wait for the Flask app to start before proceeding
until $(curl --output /dev/null --silent --head --fail http://localhost:80); do
    echo "Waiting for the Flask app to start..."
    sleep 1
done

echo "Flask app is ready! Starting socat..."

ip addr add 127.0.0.1/32 dev lo
ip link set dev lo up

# Replace these values with the desired port numbers you want to use
HOST_PORT=5000
DOCKER_PORT=80

# Route traffic from host port 5000 to Docker container port 80 using vsock
socat vsock-listen:$HOST_PORT,reuseaddr,fork tcp-connect:127.0.0.1:$DOCKER_PORT
