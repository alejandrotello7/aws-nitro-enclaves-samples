#!/bin/bash

# Pull the alpine/socat:latest Docker image
docker pull alpine/socat:latest

# Set the desired port number
PORT_NUMBER=5000

# Run the Docker container with socat
docker run -d -p $PORT_NUMBER:$PORT_NUMBER --name socat alpine/socat tcp-listen:$PORT_NUMBER,fork,keepalive,reuseaddr vsock-connect:16:5000,keepalive
