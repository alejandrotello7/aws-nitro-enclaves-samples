#!/bin/bash

# Build Docker image
docker build -t socket-sample -f Dockerfile .

# Build enclave
nitro-cli build-enclave --docker-uri socket-sample --output-file socket-sample.eif

# Run enclave
sudo nitro-cli run-enclave --cpu-count 2 --memory 2524 --enclave-cid 16 --eif-path socket-sample.eif --debug-mode

#Make setup executable
chmod +x utils/socat_ec2_host.sh

#Run the setup.sh script
./socat_ec2_host.sh



