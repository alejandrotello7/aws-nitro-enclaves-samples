#!/bin/bash
sudo docker rm enclave-runner-container
sudo docker build -t enclave_runner .
sudo docker run -p 50051:50051 -it --name enclave-runner-container enclave_runner
