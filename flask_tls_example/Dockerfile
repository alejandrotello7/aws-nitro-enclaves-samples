# Use the official Python slim image with Debian Buster as the base image
FROM ubuntu:latest

# Set the working directory to / to run the Flask app
WORKDIR /

## Install necessary packages
#RUN apt-get update && apt-get install -y \
#    iproute2 nginx curl \
#    python3 python3-pip socat \
#    zip bison build-essential cmake flex git libedit-dev \
#    libllvm14 llvm-14-dev libclang-14-dev python3-setuptools \
#    zlib1g-dev libelf-dev libfl-dev liblzma-dev libdebuginfod-dev \
#    arping netperf iperf \
#    nginx
# Install necessary packages (iproute2 for 'ip' command and socat)
RUN apt-get update && apt-get install -y iproute2 nginx curl python3 python3-pip socat git cmake clang cmake-curses-gui

# Clone the repository and build BCC
#RUN git clone https://github.com/iovisor/bcc.git \
#    && mkdir bcc/build \
#    && cd bcc/build \
#    && cmake .. \
#    && make \
#    && make install \
#    && cmake -DPYTHON_CMD=python3 .. \
#    && make \
#    && make install
#
#RUN yum install -y bpfcc-tools kernel-headers-$(uname -r)



# Install Flask and other required dependencies
RUN pip3 install Flask gunicorn cryptography grpcio grpcio-tools

# Copy files into the container
COPY app.py grpc_server.py ./
COPY utils/index.html /etc/nginx/html/index.html

COPY utils/att_doc_retriever_sample utils/attestation_retriever utils/cert.der utils/myservice.proto utils/public_enclaver_tls_key.pem utils/run.sh utils/myservice_pb2.py  ./
COPY utils/enclaves.key /etc/ssl/private/enclaves.key
COPY utils/enclaves.pem /etc/ssl/certs/enclaves.pem
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
# RUN python3 -m grpc_tools.protoc -I/app/ --python_out=/app/ --grpc_python_out=/app/ /app/myservice.proto

# Install and configure mkcert
RUN mkcert -install && \
    mkcert -cert-file enclaves_tls.pem -key-file enclaves_tls.key ec2-3-79-42-225.eu-central-1.compute.amazonaws.com

# Set execution permission for the scripts
RUN chmod +x run.sh

# Set the entry point
CMD ["./run.sh"]
