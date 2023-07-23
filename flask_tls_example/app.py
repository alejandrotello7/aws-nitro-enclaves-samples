from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Nitrogen! This is the default message."

@app.route('/api/message1')
def message1():
    return "This is message 1."

@app.route('/api/message2')
def message2():
    return "This is message 2."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)