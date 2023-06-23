#!/usr/local/bin/env python3

# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import socket
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class VsockStream:
    """Client"""

    def __init__(self, conn_tmo=5):
        self.conn_tmo = conn_tmo
        self.data = ""

    def connect(self, endpoint):
        """Connect to the remote endpoint"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.settimeout(self.conn_tmo)
        self.sock.connect(endpoint)

    def send_data(self, data):
        """Send data to a remote endpoint"""
        self.sock.sendall(data)

    def recv_data(self):
        """Receive data from a remote endpoint"""
        while True:
            data = self.sock.recv(1024).decode()
            self.data += data
            if not data:
                break
            print(data, end='', flush=True)
        self.data += ''
        print()

    def disconnect(self):
        """Close the client socket"""
        self.sock.close()


def client_handler(args):
    client = VsockStream()
    endpoint = (args.cid, args.port)
    client.connect(endpoint)
    msg = 'Hello, world!'
    client.send_data(msg.encode())
    client.disconnect()


class VsockListener:
    """Server"""

    def __init__(self, conn_backlog=128):
        self.conn_backlog = conn_backlog

    def bind(self, port):
        """Bind and listen for connections on the specified port"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.bind((socket.VMADDR_CID_ANY, port))
        self.sock.listen(self.conn_backlog)

    def recv_data(self):
        """Receive data from a remote endpoint"""
        while True:
            print("Waiting for data....")
            (from_client, (remote_cid, remote_port)) = self.sock.accept()
            # Read 1024 bytes at a time
            while True:
                try:
                    data = from_client.recv(1024).decode()
                except socket.error:
                    break
                if not data:
                    break
                print(data, end='', flush=True)
            print()
            from_client.close()

    def send_data(self, data):
        """Send data to a renote endpoint"""
        # while True:
        (to_client, (remote_cid, remote_port)) = self.sock.accept()
        to_client.sendall(data)
        to_client.close()
        return

    def decode_data(self):
        """Receive and decode data from a remote endpoint"""
        # Load the private key from file
        private_key_path = "private_key.pem"
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)

        while True:
            print("Waiting for data....")
            (from_client, (remote_cid, remote_port)) = self.sock.accept()
            # Read 1024 bytes at a time
            while True:
                try:
                    encoded_data = from_client.recv(1024)
                except socket.error:
                    break
                if not encoded_data:
                    break

                # Decode the received data
                decoded_data = private_key.decrypt(
                    encoded_data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )

                print(decoded_data.decode(), end='', flush=True)

            print()
            from_client.close()

def server_handler(args):
    server = VsockListener()
    server.bind(args.port)
    server.recv_data()


def main():
    parser = argparse.ArgumentParser(prog='vsock-sample')
    parser.add_argument("--version", action="version",
                        help="Prints version information.",
                        version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(title="options")

    client_parser = subparsers.add_parser("client", description="Client",
                                          help="Connect to a given cid and port.")
    client_parser.add_argument("cid", type=int, help="The remote endpoint CID.")
    client_parser.add_argument("port", type=int, help="The remote endpoint port.")
    client_parser.set_defaults(func=client_handler)

    server_parser = subparsers.add_parser("server", description="Server",
                                          help="Listen on a given port.")
    server_parser.add_argument("port", type=int, help="The local port to listen on.")
    server_parser.set_defaults(func=server_handler)

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
