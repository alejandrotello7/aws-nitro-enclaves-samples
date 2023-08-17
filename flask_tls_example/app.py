import base64
import json
import threading

from flask import Flask, request, jsonify, send_file
import subprocess as sp
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pickle
import grpc
import myservice_pb2
import myservice_pb2_grpc
from concurrent import futures
import sys
import logging

app = Flask(__name__)
attested_document_server = None
attested_document_valid_options = \
    {'pcrs',
     'nonce',
     'module_id',
     'public_key',
     'private_key_path',
     'public_key_path'}


class GreetService(myservice_pb2_grpc.MyServiceServicer):
    def Execute(self, request, context):
        # Deserialize the function and arguments using pickle
        function_to_execute = pickle.loads(request.function)
        arguments = pickle.loads(request.arguments)

        # Execute the function with provided arguments
        result = function_to_execute(*arguments)

        # Serialize the result using pickle
        serialized_result = pickle.dumps(result)

        # Create the response and return it
        return myservice_pb2.ExecuteResponse(result=serialized_result)


def run_grpc_server():
    # Load your certificate and key files (replace 'certificate.pem' and 'key.pem' with the actual file paths)
    with open('/etc/ssl/certs/enclaves.pem', 'rb') as f:
        certificate = f.read()
    with open('/etc/ssl/private/enclaves.key', 'rb') as f:
        private_key = f.read()

    # Create TLS credentials from the certificate and key
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate,),))

    # Create the gRPC server with the TLS credentials
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    myservice_pb2_grpc.add_MyServiceServicer_to_server(GreetService(), server)
    server.add_secure_port('[::]:50051', server_credentials)
    # Log a message indicating that the server is running
    logger = logging.getLogger('grpc_server')
    logger.setLevel(logging.INFO)

    # Log to console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    server.start()
    logger.info("gRPC server is running on port 50051...")

    server.wait_for_termination()


@app.route('/')
def index():
    return "Hello from the enclave! This is the default message."


@app.route('/api/attestation')
def attestation():
    global attested_document_server
    current_dir = os.path.dirname(os.path.abspath(__file__))
    rs_binary = os.path.join(current_dir, 'att_doc_retriever_sample')
    proc = sp.Popen([rs_binary], stdout=sp.PIPE)
    out, err = proc.communicate()
    attested_document_server = json.loads(out)
    return attested_document_server


@app.route('/api/attestation_retriever/<arg>')
def attestation_retriever(arg):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    rs_binary = os.path.join(current_dir, 'attestation_retriever')
    proc = sp.Popen([rs_binary, arg], stdout=sp.PIPE)
    out, err = proc.communicate()
    return out.rstrip()
    # response_file = os.path.join(current_dir, 'response.txt')
    # if os.path.exists(response_file):
    #     response = send_file(response_file)
    #     response.headers['Content-Disposition'] = 'attachment; filename=response.txt'
    #     return response
    # else:
    #     return "Response file not found"
    #
    # # Remove trailing whitespace and newlines
    # out = out.rstrip()
    # return out



@app.route('/api/execute', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Save the uploaded file
        file_path = os.path.join(os.getcwd(), 'uploaded_file.bin')
        file.save(file_path)

        # Make the file executable (optional, depending on your use case)
        os.chmod(file_path, 0o755)

        try:
            # Execute the uploaded binary file
            proc = sp.Popen([file_path], stdout=sp.PIPE, stderr=sp.PIPE)
            out, err = proc.communicate()
            return jsonify({"stdout": out.decode('utf-8'), "stderr": err.decode('utf-8')}), 200
        except Exception as e:
            return jsonify({"error": f"Error executing binary: {str(e)}"}), 500

    else:
        return jsonify({"error": "No file received."}), 400


@app.route('/api/attestation/<arg>', methods=['GET'])
def get_attested_arg(arg):
    global attested_document_server  # Access the global variable
    global attested_document_valid_options  # Access valid options globally

    # Check if attestation has been performed
    if attested_document_server is not None:
        # Check if the provided argument is in the set of valid options
        if arg in attested_document_valid_options:
            return jsonify({arg: attested_document_server[arg]})
        else:
            return jsonify({
                "error": f"Invalid argument '{arg}'. Valid options are: {', '.join(attested_document_valid_options)}"}), 400
    else:
        return jsonify({"error": "Attestation not performed yet."}), 400


@app.route('/api/decode', methods=['POST'])
def decode_message():
    global attested_document_server
    # Get the encoded message from the request
    encoded_message = request.form.get('encoded_message')
    if not encoded_message:
        return jsonify({"error": "Encoded message not provided."}), 400

    # Retrieve the private key path from attested_document_server
    private_key_path = attested_document_server['private_key_path']

    try:
        # Load the private key from the file
        with open(private_key_path, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )

        # Convert the encoded message from hexadecimal to bytes
        encoded_message_bytes = bytes.fromhex(encoded_message)

        # Decrypt the message using the private key
        decrypted_message = private_key.decrypt(
            encoded_message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Return the decrypted message as a response
        return jsonify({"decrypted_message": decrypted_message.decode('utf-8')}), 200

    except Exception as e:
        return jsonify({"error": f"Error decoding message: {str(e)}"}), 500


@app.route('/api/message2')
def message2():
    return "This is message 2."


@app.route('/api/public_certificate')
def retrieve_public_certificate():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Read the public key from public_enclaver_tls_key.pem
    public_key_path = os.path.join(current_dir, 'public_enclaver_tls_key.pem')
    with open(public_key_path, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    file_path = os.path.join(current_dir, 'enclaves_tls.pem')
    try:
        with open(file_path, 'rb') as file:
            certificate_content = file.read()
            print("Certificate content:", certificate_content)  # Debug: Print the certificate content
            encrypted_content = public_key.encrypt(
                certificate_content,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return encrypted_content
    except Exception as e:
        return f"Error reading or encrypting certificate: {str(e)}", 500

if __name__ == '__main__':
    print('Starting flask app...')
    attestation()
    # Start the gRPC server in a separate thread
    # server_thread = threading.Thread(target=run_grpc_server)
    # server_thread.start()
    app.run(host='0.0.0.0', port=8000)
