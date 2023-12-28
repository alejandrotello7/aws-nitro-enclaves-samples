#!/bin/bash

# Build Docker image
docker build -t nginx-sample -f Dockerfile .

# Build enclave
nitro-cli build-enclave --docker-uri nginx-sample --output-file nginx-sample.eif

# Run enclave
sudo nitro-cli run-enclave --cpu-count 2 --memory 2524 --enclave-cid 16 --eif-path nginx-sample.eif --debug-mode

#Make setup executable
chmod +x utils/setup.sh

#Run the setup.sh script
./utils/setup.sh



