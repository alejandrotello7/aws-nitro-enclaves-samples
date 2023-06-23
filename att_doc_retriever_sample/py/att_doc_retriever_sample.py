#!/usr/local/bin/env python3

# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import argparse
import inspect
import json
import subprocess as sp
import sys
from os import path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# import file from different location
current_dir = path.dirname(path.abspath(inspect.getfile(inspect.currentframe())))
vsock_dir = path.join(path.dirname(path.dirname(current_dir)), 'vsock_sample/py')
sys.path.insert(0, vsock_dir)
vs = __import__('vsock-sample')

# Binary executed
# RS_BINARY = path.join(current_dir, 'att_doc_retriever_sample')
RS_BINARY = path.join(current_dir, 'att_doc_retriever_sample')


def encode_message(message, public_key_path):
    # Load the public key from file
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    # Encode the message
    encoded_message = public_key.encrypt(
        message.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encoded_message


def decode_message(encoded_message, private_key_path):
    # Load the private key from file
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    # Decode the message
    decoded_message = private_key.decrypt(
        encoded_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decoded_message.decode("utf-8")

def write_string_to_file(string, file_path):
    try:
        with open(file_path, "w") as file:
            file.write(string)
        print("String successfully written to file.")
    except IOError:
        print("An error occurred while writing to the file.")

def client_handler(args):
    client = vs.VsockStream()
    endpoint = (args.cid, args.port)
    client.connect(endpoint)
    client.recv_data()
    attested_document = json.loads(client.data)
    print(f"PCRS: {attested_document['pcrs']}\n")
    print(f"Module Id: {attested_document['module_id']}\n")
    print(f"Nonce: {attested_document['nonce']}\n")
    print(f"Public Key: {attested_document['public_key']}\n")

    public_key = attested_document['public_key']
    file_path = "public_key.pem"
    write_string_to_file(public_key, file_path)

    client.disconnect()


def server_handler(args):
    server = vs.VsockListener()
    server.bind(args.port)

    # Execute binary and send the output to client
    proc = sp.Popen([RS_BINARY], stdout=sp.PIPE)
    out, err = proc.communicate()

    # Testing private key logic
    attested_document_server = json.loads(out)
    print(f"Private Key Path: {attested_document_server['private_key_path']}\n")
    print(f"Public Key Path: {attested_document_server['public_key_path']}\n")

    public_key_path = "public_key.pem"
    message = "Hello, world!"
    encoded_message = encode_message(message, public_key_path)
    private_key_path = "private_key.pem"
    decoded_message = decode_message(encoded_message, private_key_path)

    print(f"Normal Message: {message}\n")
    print(f"Encoded Message: {encoded_message}\n")
    print(f"Decoded Message: {decoded_message}\n")

    server.send_data(out)
    print("Server Connection Closed")

def decoder_handler(args):
    server = vs.VsockListener()
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
    # client_parser.add_argument("pcr0", help="PCR0 value of the enclave image. ")
    client_parser.set_defaults(func=client_handler)

    server_parser = subparsers.add_parser("server", description="Server",
                                          help="Listen on a given port.")
    server_parser.add_argument("port", type=int, help="The local port to listen on.")
    server_parser.set_defaults(func=server_handler)

    decoder_parser = subparsers.add_parser("decoder", description="Decoder Process", help="Test process")
    decoder_parser.add_argument("port", type=int, help="The local port to listen on.")
    server_parser.set_defaults(func=decoder_handler)


    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
