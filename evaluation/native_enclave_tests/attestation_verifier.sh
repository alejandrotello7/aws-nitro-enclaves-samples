#!/bin/bash

logfile="attestation_document_requester.log"
total_time=0
runs=10

echo "Attestation Requester Document Time Measurements" > "$logfile"
echo "--------------------------------" >> "$logfile"

for i in $(seq 1 $runs)
do

    start_time=$(date +%s.%N)

    # Run the setup script
    cargo run

    end_time=$(date +%s.%N)
    elapsed=`echo "$end_time - $start_time" | bc`
    total_time=`echo "$total_time + $elapsed" | bc`
    echo "Run $i: $elapsed seconds" | tee -a "$logfile"
done

# Calculate the average time
average_time=`echo "scale=3; $total_time / $runs" | bc`
echo "--------------------------------" >> "$logfile"
echo "Average time over $runs runs: $average_time seconds" | tee -a "$logfile"
