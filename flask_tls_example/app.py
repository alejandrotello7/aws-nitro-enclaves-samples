import json

from flask import Flask
import subprocess as sp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Nitrogen! This is the default message."

@app.route('/api/attestation')
def message1():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    rs_binary = os.path.join(current_dir, 'att_doc_retriever_sample')
    proc = sp.Popen([rs_binary], stdout=sp.PIPE)
    out, err = proc.communicate()
    attested_document_server = json.loads(out)
    return attested_document_server

@app.route('/api/message2')
def message2():
    return "This is message 2."

if __name__ == '__main__':
    print('Starting flask app...')
    app.run(host='0.0.0.0', port=80)