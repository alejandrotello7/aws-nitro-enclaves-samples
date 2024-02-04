#!/bin/bash

logfile="enclave_docker_image_build_times.log"
total_time=0
runs=10

echo "Enclave Docker Image Build Time Measurements" > "$logfile"
echo "--------------------------------" >> "$logfile"

for i in $(seq 1 $runs)
do
    # Delete existing Docker image
    docker rmi nginx-sample

    start_time=$(date +%s.%N)

    # Build the image
    docker build -t nginx-sample -f Dockerfile .

    end_time=$(date +%s.%N)
    elapsed=`echo "$end_time - $start_time" | bc`
    total_time=`echo "$total_time + $elapsed" | bc`
    echo "Docker build $i: $elapsed seconds" | tee -a "$logfile"
done

# Calculate the average time
average_time=`echo "scale=3; $total_time / $runs" | bc`
echo "--------------------------------" >> "$logfile"
echo "Average time over $runs runs: $average_time seconds" | tee -a "$logfile"

To get this measurement, we ran a script calling the commands needed to boot a Nitro Enclave from an EC2 instance and timed the execution time:
\begin{enumerate}
\item  \texttt{nitro-cli build-enclave --docker-uri nginx-sample --output-file nginx-sample.eif}
\item \texttt{sudo nitro-cli run-enclave --cpu-count 2 --memory 2588 --enclave-cid 16 --eif-path nginx-sample.eif}
\end{enumerate}