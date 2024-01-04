#!/bin/bash

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <Instance2-IP-or-Domain>"
    exit 1
fi

INSTANCE_2_ADDRESS=$1

# Step 1: Generate Certificates
mkcert -cert-file enclaves.pem -key-file enclaves.key "$INSTANCE_2_ADDRESS"

# Step 2: Copy Certificates
cp enclaves.pem enclaves.key /path/to/aws-nitro-enclaves-samples/flask_tls_example/utils/

# Step 3: Git Operations
cd /path/to/aws-nitro-enclaves-samples
git add flask_tls_example/utils/enclaves.pem flask_tls_example/utils/enclaves.key
git commit -m "Add SSL certificates"
git push origin main
