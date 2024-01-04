#!/bin/bash

# Navigate to Python script directory and execute it
cd /home/ec2-user/dev/aws-nitro-enclaves-samples/enclave_runner/
python3_output=$(python3 spawner_client.py)
echo "$python3_output"

# Extract and save pcr0 and enclave_id
pcr0=$(echo "$python3_output" | grep "PCR0" | cut -d' ' -f2)
pcr1=$(echo "$python3_output" | grep "PCR1" | cut -d' ' -f2)
pcr2=$(echo "$python3_output" | grep "PCR2" | cut -d' ' -f2)
enclave_id=$(echo "$python3_output" | grep "EnclaveID" | cut -d' ' -f2)

# Navigate to Rust program directory and run it (A delayed of 10s is used to ensure enclave is up)
sleep 10
cd /home/ec2-user/dev/aws-nitro-enclaves-samples/att_doc_verifier
cargo_output=$(cargo run)
echo "$cargo_output"

# Use jq to parse the JSON output and extract PCR0 and Module ID
rust_pcr0=$(echo "$cargo_output" | jq -r '.pcrs.PCR0')
rust_pcr1=$(echo "$cargo_output" | jq -r '.pcrs.PCR1')
rust_pcr2=$(echo "$cargo_output" | jq -r '.pcrs.PCR2')
rust_module_id=$(echo "$cargo_output" | jq -r '.module_id')


# Add your logic for comparing with stored pcr0 and module_id
rust_pcr0_lower=$(echo "$rust_pcr0" | tr '[:upper:]' '[:lower:]')
rust_pcr1_lower=$(echo "$rust_pcr1" | tr '[:upper:]' '[:lower:]')
# Print the extracted values
echo "Extracted PCR0: $rust_pcr0_lower"
echo "Extracted PCR1: $rust_pcr1_lower"

echo "Extracted Module ID: $rust_module_id"


if [[ "$pcr0" == "$rust_pcr0_lower" && "$pcr1" == "$rust_pcr1_lower" ]]; then
    echo "Success: Verification passed."
else
    echo "Failed: Verification failed."
fi