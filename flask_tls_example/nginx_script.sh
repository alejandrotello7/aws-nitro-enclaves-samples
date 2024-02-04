#!/bin/bash

# Build Docker image
docker build --no-cache -t nginx-sample -f Dockerfile .

# Build enclave
ENCLAVE_OUTPUT=$(nitro-cli build-enclave --docker-uri nginx-sample --output-file nginx-sample.eif)

# Extract PCR0
PCR0=$(echo "$ENCLAVE_OUTPUT" | jq -r '.Measurements.PCR0')
echo "PCR0: $PCR0"

# Run enclave
RUN_OUTPUT=$(sudo nitro-cli run-enclave --cpu-count 2 --memory 2704 --enclave-cid 16 --eif-path nginx-sample.eif)

# Extract EnclaveID
ENCLAVE_ID=$(echo "$RUN_OUTPUT" | jq -r '.EnclaveID')
echo "EnclaveID: $ENCLAVE_ID"

# Make setup executable
chmod +x utils/setup.sh

# Run the setup.sh script
./utils/setup.sh
