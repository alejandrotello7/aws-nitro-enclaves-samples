from flask import Flask, jsonify
import subprocess
import json

app = Flask(__name__)


@app.route('/start_enclave', methods=['GET'])
def start_enclave():
    try:
        # Running the script and capturing its output
        script_output = subprocess.check_output(['/home/ec2-user/dev/aws-nitro-enclaves-samples/flask_tls_example/nginx_script.sh'], shell=True).decode()

        # Parse the output to extract EnclaveID and PCR0
        output_lines = script_output.split('\n')
        enclave_id = next(line.split(': ')[1] for line in output_lines if "EnclaveID" in line)
        pcr0 = next(line.split(': ')[1] for line in output_lines if "PCR0" in line)

        return jsonify({"EnclaveID": enclave_id, "PCR0": pcr0}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50052)
