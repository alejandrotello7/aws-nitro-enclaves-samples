#!/bin/bash

# Pull the alpine/socat:latest Docker image
docker pull alpine/socat:latest

# Set the desired port number
PORT_NUMBER=5000
REGULAR_PORT=80

# Run the Docker container with socat
docker run -d -p $PORT_NUMBER:$PORT_NUMBER --name socat_$PORT_NUMBER alpine/socat tcp-listen:$PORT_NUMBER,fork,keepalive,reuseaddr vsock-connect:16:5000,keepalive

docker run -d -p $REGULAR_PORT:$REGULAR_PORT --name socat_$REGULAR_PORT alpine/socat tcp-listen:$REGULAR_PORT,fork,keepalive,reuseaddr vsock-connect:16:80,keepalive

socat vsock-listen:6000,reuseaddr,fork tcp-connect:18.156.117.254:50051 &
