#!/bin/bash

logfile="code_execution_test.log"
total_time=0
runs=10

echo "Code execution Time Measurements" > "$logfile"
echo "--------------------------------" >> "$logfile"

for i in $(seq 1 $runs)
do

    start_time=$(date +%s.%N)

    # Run the setup script
    curl -X POST -F "file=@/usr/src/app/enclave_runner/tester_enclave_runner" https://ec2-3-70-8-55.eu-central-1.compute.amazonaws.com:5000/api/execute_interceptor

    end_time=$(date +%s.%N)
    elapsed=`echo "$end_time - $start_time" | bc`
    total_time=`echo "$total_time + $elapsed" | bc`
    echo "Run $i: $elapsed seconds" | tee -a "$logfile"
done

# Calculate the average time
average_time=`echo "scale=3; $total_time / $runs" | bc`
echo "--------------------------------" >> "$logfile"
echo "Average time over $runs runs: $average_time seconds" | tee -a "$logfile"
