from flask import Flask

app = Flask(__name__)

@app.route('/')
def init():
    return 'Hello Phuong!'

app.run(host='0.0.0.0', port=5000)