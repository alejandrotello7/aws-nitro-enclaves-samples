#!/bin/bash

# Build Docker image
docker build -t att-doc-retriever-sample -f Dockerfile --build-arg ARCH=$(uname -m) ..

# Build enclave
nitro-cli build-enclave --docker-uri att-doc-retriever-sample --output-file att_doc_retriever_sample.eif

# Run enclave
sudo nitro-cli run-enclave --cpu-count 2 --memory 1940 --enclave-cid 16 --eif-path att_doc_retriever_sample.eif --debug-mode

# Run Python script
python3 py/att_doc_retriever_sample.py tls_client 16 5010

