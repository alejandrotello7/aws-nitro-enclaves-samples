#!/bin/bash

# Build Docker image
docker build -t nginx-sample -f Dockerfile .

# Build enclave
nitro-cli build-enclave --docker-uri nginx-sample --output-file nginx-sample.eif

# Run enclave


#Make setup executable
chmod +x utils/setup.sh

#Run the setup.sh script
./utils/setup.sh



