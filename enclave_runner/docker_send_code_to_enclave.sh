#!/bin/bash

# Assuming the socket_tester directory and tester_enclave_runner are copied into the container
cd /usr/src/app/enclave_runner/socket_tester
python3 socket_server.py &

# Allow some time for the socket server to start
sleep 5

# Replace the file path with the correct path in the container
# Also, update the URL if needed, especially if it refers to a service outside the container
curl -X POST -F "file=@/usr/src/app/enclave_runner/tester_enclave_runner" https://ec2-3-70-8-55.eu-central-1.compute.amazonaws.com:5000/api/execute_interceptor
