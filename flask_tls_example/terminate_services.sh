#!/bin/bash

# Terminate all enclaves
sudo nitro-cli terminate-enclave --all

# Stop and remove the Docker container 'alpine/socat'
docker stop socat
docker rm socat