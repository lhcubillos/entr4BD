from flask import Flask
# create the little application object
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'
