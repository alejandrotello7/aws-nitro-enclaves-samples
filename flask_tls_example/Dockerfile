# Use the official Python slim image with Debian Buster as the base image
FROM ubuntu:latest

# Set the working directory to / to run the Flask app
WORKDIR /

# Install necessary packages
RUN apt-get update && apt-get install -y \
    iproute2 nginx curl \
    python3 python3-pip socat \
    zip bison build-essential cmake flex git libedit-dev \
    libllvm14 llvm-14-dev libclang-14-dev python3-setuptools \
    zlib1g-dev libelf-dev libfl-dev liblzma-dev libdebuginfod-dev \
    arping netperf iperf \
    nginx

# Clone the repository and build BCC
RUN git clone https://github.com/iovisor/bcc.git \
    && cd bcc/build \
    && cmake .. \
    && make \
    && sudo make install

# Build Python3 bindings
RUN cd /bcc/build/src/python \
    && cmake -DPYTHON_CMD=python3 .. \
    && make \
    && sudo make install

# Install Flask and other required dependencies
RUN pip3 install Flask gunicorn cryptography grpcio grpcio-tools

# Copy files into the container
COPY app.py grpc_server.py utils/ /app/
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Expose ports
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
RUN python3 -m grpc_tools.protoc -I/app/ --python_out=/app/ --grpc_python_out=/app/ /app/myservice.proto

# Install and configure mkcert
RUN mkcert -install && \
    mkcert -cert-file /app/enclaves_tls.pem -key-file /app/enclaves_tls.key ec2-3-79-42-225.eu-central-1.compute.amazonaws.com

# Set execution permission for the scripts
RUN chmod +x /app/run.sh

# Set the entry point
CMD ["/app/run.sh"]
