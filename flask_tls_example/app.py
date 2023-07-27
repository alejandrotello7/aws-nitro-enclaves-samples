import base64
import json

from flask import Flask, request, jsonify
import subprocess as sp
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pickle

app = Flask(__name__)
attested_document_server = None
attested_document_valid_options = \
    {'pcrs',
     'nonce',
     'module_id',
     'public_key',
     'private_key_path',
     'public_key_path'}


def execute_function(function_name, module_name, serialized_arguments):
    # Decode Base64 strings back to bytes
    function_name_bytes = base64.b64decode(function_name.encode())
    module_name_bytes = base64.b64decode(module_name.encode())
    arguments_bytes = base64.b64decode(serialized_arguments.encode())

    # Deserialize the function name and module using pickle
    function_name = pickle.loads(function_name_bytes)
    module_name = pickle.loads(module_name_bytes)

    # Import the module dynamically
    module = __import__(module_name, fromlist=[function_name])
    function_to_execute = getattr(module, function_name)

    # Deserialize the arguments using pickle
    arguments = pickle.loads(arguments_bytes)

    # Execute the function with provided arguments
    result = function_to_execute(*arguments)
    return result


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


@app.route('/api/remote_function', methods=['POST'])
def handle_remote_function():
    # Get the Base64-encoded function name, module, and arguments from the request data
    function_name_base64 = request.form['function_name']
    module_name_base64 = request.form['module_name']
    arguments_base64 = request.form['arguments']

    # Execute the function and get the result
    result = execute_function(function_name_base64, module_name_base64, arguments_base64)
    print(result)

    # Serialize the result using pickle
    serialized_result = pickle.dumps(result)

    return serialized_result

if __name__ == '__main__':
    print('Starting flask app...')
    attestation()
    app.run(host='0.0.0.0', port=8000)
