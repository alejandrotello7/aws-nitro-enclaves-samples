#!/bin/bash

logfile="enclave_run_times.log"
total_time=0
runs=5

echo "Enclave Run Time Measurements" > "$logfile"
echo "--------------------------------" >> "$logfile"

for i in $(seq 1 $runs)
do
    # Terminate any running enclave before starting a new one
    sudo nitro-cli terminate-enclave --all

    start_time=$(date +%s.%N)

    # Run the enclave
    sudo nitro-cli run-enclave --cpu-count 2 --memory 2588 --enclave-cid 16 --eif-path nginx-sample.eif

    end_time=$(date +%s.%N)
    elapsed=`echo "$end_time - $start_time" | bc`
    total_time=`echo "$total_time + $elapsed" | bc`
    echo "Run $i: $elapsed seconds" | tee -a "$logfile"
done

# Calculate the average time
average_time=`echo "scale=3; $total_time / $runs" | bc`
echo "--------------------------------" >> "$logfile"
echo "Average time over $runs runs: $average_time seconds" | tee -a "$logfile"

# Ensure the last enclave is terminated
sudo nitro-cli terminate-enclave --all
