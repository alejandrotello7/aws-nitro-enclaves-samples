#!/bin/bash

# Navigate to Python script directory and execute it
cd /home/ec2-user/dev/aws-nitro-enclaves-samples/enclave_runner/
python3_output=$(python3 spawner_client.py)
echo "$python3_output"

# Extract and save pcr0 and enclave_id
pcr0=$(echo "$python3_output" | grep "PCR0" | cut -d' ' -f2)
enclave_id=$(echo "$python3_output" | grep "EnclaveID" | cut -d' ' -f2)

# Navigate to Rust program directory and run it (A delayed of 10s is used to ensure enclave is up)
sleep 10
cd /home/ec2-user/dev/aws-nitro-enclaves-samples/att_doc_verifier
cargo_output=$(cargo run)
echo "$cargo_output"

# Extract pcr0 and module_id from Rust program output
rust_pcr0=$(echo "$cargo_output" | grep "\"PCR0\"" | cut -d':' -f2 | tr -d ' ",')
rust_module_id=$(echo "$cargo_output" | grep "module_id" | cut -d':' -f2 | tr -d ' ",')

# Compare and output results
if [[ "$enclave_id" == "$rust_module_id" ]]; then
    echo "Success: Verification passed"
else
    echo "Failed: Verification failed due to mismatch"
    echo $enclave_id
    echo $rust_module_id

fi
