# Use the official Python slim image with Debian Buster as the base image
FROM ubuntu:latest

# Set the working directory to / to run the Flask app
WORKDIR /

# Install necessary packages (iproute2 for 'ip' command and socat)
RUN apt-get update && apt-get install -y iproute2 nginx curl
RUN apt-get update && apt-get install -y python3 python3-pip socat

RUN apt-get update && apt-get install -y \
    iproute2 \
    nginx \
    curl \
    python3 \
    python3-pip \
    socat \
    zip \
    bison \
    build-essential \
    cmake \
    flex \
    git \
    libedit-dev \
    libllvm14 \
    llvm-14-dev \
    libclang-14-dev \
    python3-setuptools \
    zlib1g-dev \
    libelf-dev \
    libfl-dev \
    liblzma-dev \
    libdebuginfod-dev \
    arping \
    netperf \
    iperf

#RUN apt-get install -y zip bison build-essential cmake flex git libedit-dev \
#  libllvm14 llvm-14-dev libclang-14-dev python3 zlib1g-dev libelf-dev libfl-dev python3-setuptools \
#  liblzma-dev libdebuginfod-dev arping netperf iperf \

# Install Flask and other required dependencies
RUN pip3 install Flask gunicorn
RUN pip3 install cryptography grpcio grpcio-tools

# Copy the app.py file into the container
COPY app.py .
COPY grpc_server.py .
COPY utils/index.html /etc/nginx/html/index.html

# Copy Nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Copy Rust binary and Amazon certificate
COPY utils/att_doc_retriever_sample .
COPY utils/attestation_retriever .
COPY utils/cert.der .
COPY utils/myservice.proto .
COPY utils/public_enclaver_tls_key.pem .

# Copy the run.sh script into the container
COPY utils/run.sh .

# Copy certificate and key
COPY utils/enclaves.key /etc/ssl/private/enclaves.key
COPY utils/enclaves.pem /etc/ssl/certs/enclaves.pem

# Expose port 8000 to allow communication with the Flask app
EXPOSE 8000
EXPOSE 443
EXPOSE 80
EXPOSE 50051
EXPOSE 50052

# Download mkcert binary
RUN curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64" && \
    chmod +x mkcert-v*-linux-amd64 && \
    mv mkcert-v*-linux-amd64 /usr/local/bin/mkcert

# Generate Python files from the proto definition
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. myservice.proto

RUN mkcert -install
RUN mkcert -cert-file enclaves_tls.pem -key-file enclaves_tls.key ec2-3-79-42-225.eu-central-1.compute.amazonaws.com


# Set execution permission for the scripts
RUN chmod +x run.sh


CMD ["./run.sh"]


# Run the Flask app using the built-in development server
#CMD ["python3", "app.py"]