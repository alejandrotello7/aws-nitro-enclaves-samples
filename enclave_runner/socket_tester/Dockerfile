# Use the official Python slim image with Debian Buster as the base image
FROM ubuntu:latest

# Set the working directory to / to run the Flask app
WORKDIR /

RUN apt-get update && apt-get install -y iproute2 nginx curl python3 python3-pip socat git cmake libcapstone4


# Copy files into the container
COPY tester_socket3 client.py run.sh ./
#COPY utils/index.html /etc/nginx/html/index.html

#COPY utils/att_doc_retriever_sample utils/attestation_retriever utils/cert.der utils/myservice.proto utils/public_enclaver_tls_key.pem utils/run.sh ./
#COPY utils/enclaves.key /etc/ssl/private/enclaves.key
#COPY utils/enclaves.pem /etc/ssl/certs/enclaves.pem
#COPY nginx/nginx.conf /etc/nginx/nginx.conf
#COPY utils/syscall_intercept/ ./syscall_intercept/

# Expose ports
EXPOSE 8000
EXPOSE 443
EXPOSE 80
EXPOSE 50051
EXPOSE 50052

## Download mkcert binary
#RUN curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64" && \
#    chmod +x mkcert-v*-linux-amd64 && \
#    mv mkcert-v*-linux-amd64 /usr/local/bin/mkcert
#
## Generate Python files from the proto definition
## RUN python3 -m grpc_tools.protoc -I/app/ --python_out=/app/ --grpc_python_out=/app/ /app/myservice.proto
#
## Install and configure mkcert
#RUN mkcert -install && \
#    mkcert -cert-file enclaves_tls.pem -key-file enclaves_tls.key ec2-3-71-30-100.eu-central-1.compute.amazonaws.com


# Set execution permission for the scripts
RUN chmod +x run.sh

# Set the entry point
CMD ["./run.sh"]
