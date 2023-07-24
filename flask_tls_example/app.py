import json

from flask import Flask, request, jsonify
import subprocess as sp
import os

app = Flask(__name__)
attested_document_server = None
ATTESTED_DOCUMENT_VALID_OPTIONS = \
    {'pcrs',
     'nonce',
     'module_id',
     'public_key',
     'private_key_path',
     'public_key_path'}


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
    global ATTESTED_DOCUMENT_VALID_OPTIONS  # Access valid options globally

    # Check if attestation has been performed
    if attested_document_server is not None:
        # Check if the provided argument is in the set of valid options
        if arg in ATTESTED_DOCUMENT_VALID_OPTIONS:
            return jsonify({arg: attested_document_server[arg]})
        else:
            return jsonify({
                               "error": f"Invalid argument '{arg}'. Valid options are: {', '.join(ATTESTED_DOCUMENT_VALID_OPTIONS)}"}), 400
    else:
        return jsonify({"error": "Attestation not performed yet."}), 400


@app.route('/api/message2')
def message2():
    return "This is message 2."


if __name__ == '__main__':
    print('Starting flask app...')
    attestation()
    app.run(host='0.0.0.0', port=80)
