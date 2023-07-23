#!/bin/bash

# Terminate all enclaves
sudo nitro-cli terminate-enclave --all

# Stop and remove the Docker container 'alpine/socat'
docker stop $(docker ps -q --filter ancestor=alpine/socat)
docker rm $(docker ps -aq --filter ancestor=alpine/socat)