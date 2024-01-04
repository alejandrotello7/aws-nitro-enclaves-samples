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

# Extract pcr0 and module_id from the Rust program output
rust_pcr0=$(echo "$cargo_output" | awk -F'[:,]' '/"PCR0"/ {gsub(/[^0-9a-fA-F]/, "", $2); print $2}')
rust_module_id=$(echo "$cargo_output" | awk -F'[:,]' '/"module_id"/ {gsub(/[^0-9a-zA-Z-]/, "", $2); print $2}')

# Print the extracted values
echo "Extracted PCR0: $rust_pcr0"
echo "Extracted Module ID: $rust_module_id"

# Add your logic for comparing with stored pcr0 and module_id
stored_pcr0="your_stored_pcr0_value"
stored_module_id="your_stored_module_id_value"

if [[ "$rust_module_id" == "$stored_module_id" ]]; then
    echo "Success: Verification passed."
else
    echo "Failed: Verification failed."
fi