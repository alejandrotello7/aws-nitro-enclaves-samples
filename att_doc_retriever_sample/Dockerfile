# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

#FROM ubuntu:latest AS builder
#WORKDIR /root/att_doc_retriever_sample/rs/
#ARG ARCH
#
## Ensure the architecture is set
#RUN if [ -n "${ARCH}" ]; \
#    then echo "Will target architecture \"${ARCH}\"."; \
#    else echo "Target architecture not specified. Will exit."; exit 1; \
#    fi
#
#COPY att_doc_retriever_sample/rs .
#RUN apt-get update && apt-get install gcc curl -y\
#    && apt-get install musl-tools -y\
#    && apt-get install libssl-dev -y
#
##ENV OPENSSL_LIB_DIR="/usr/lib/ssl"
##ENV OPENSSL_INCLUDE_DIR = "/usr/include/openssl"UNAME -M
##RUN echo $OPENSSL_DIR
##RUN apt-get install perl
## Get Rust
#RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
#ENV PATH="/root/.cargo/bin:${PATH}"
#RUN rustup target install ${ARCH}-unknown-linux-musl
#
##RUN openssl version -d
##ENV PKG_CONFIG_SYSROOT_DIR=/
##ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig
##RUN echo $PKG_CONFIG_SYSROOT_DIR
#
## Build the Rust application
#RUN cargo build --release --target=${ARCH}-unknown-linux-musl

#FROM python:3.7.9-alpine3.12
FROM ubuntu:latest
WORKDIR /root/att_doc_retriever_sample/py/
ARG ARCH
RUN apt-get update && apt-get install gcc curl -y

# Get Rust
#RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
#
#ENV PATH="/root/.cargo/bin:${PATH}"
#RUN rustup target install ${ARCH}-unknown-linux-musl

#RUN apk update
#RUN apk add --no-cache \
##    build-base \
#    libffi-dev \
#    openssl-dev \
#    cargo
RUN apt-get install -y python3
RUN apt-get install python3-pip -y
RUN pip install cryptography

# Copy the Rust compiled binary from previous image
#COPY --from=builder /root/att_doc_retriever_sample/rs/target/${ARCH}-unknown-linux-musl/release/att_doc_retriever_sample .
# Copy the python client-server handler logic to the container
COPY att_doc_retriever_sample/py/att_doc_retriever_sample .
COPY att_doc_retriever_sample/py/att_doc_retriever_sample.py .
COPY att_doc_retriever_sample/py/cert.der .
COPY att_doc_retriever_sample/py/fake_cert.der .

# Copy the client-server logic from the vsock sample to the container
COPY vsock_sample/py/vsock-sample.py /root/vsock_sample/py/

# Copy the tlser logic to the container
COPY tls_connection_sample/py/tls_connection_sample.py /root/vsock_sample/py/

# 5010 is the socket port
#CMD ["python3", "/root/att_doc_retriever_sample/py/att_doc_retriever_sample.py", "server", "5010"]
CMD ["python3", "/root/att_doc_retriever_sample/py/att_doc_retriever_sample.py", "tls_server", "5010"]
