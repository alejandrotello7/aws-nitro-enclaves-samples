# app.py
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/start_enclave', methods=['GET'])
def start_enclave():
    try:
        # Replace 'your_script.sh' with your actual script name
        result = subprocess.check_output(['./your_script.sh'], shell=True)
        return jsonify({"message": "Enclave started", "data": result.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
