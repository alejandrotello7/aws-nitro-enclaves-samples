#!/bin/bash

logfile="setup_build_times.log"
total_time=0
runs=10

echo "Setup build Time Measurements" > "$logfile"
echo "--------------------------------" >> "$logfile"

for i in $(seq 1 $runs)
do
    # Kill socat and docker containers
    ./terminate_services.sh
    pkill socat


    start_time=$(date +%s.%N)

    # Run the setup script
    ./setup.sh

    end_time=$(date +%s.%N)
    elapsed=`echo "$end_time - $start_time" | bc`
    total_time=`echo "$total_time + $elapsed" | bc`
    echo "Run $i: $elapsed seconds" | tee -a "$logfile"
done

# Calculate the average time
average_time=`echo "scale=3; $total_time / $runs" | bc`
echo "--------------------------------" >> "$logfile"
echo "Average time over $runs runs: $average_time seconds" | tee -a "$logfile"

./terminate_services.sh
pkill socat