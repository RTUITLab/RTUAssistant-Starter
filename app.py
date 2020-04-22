from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index page'

@app.route('/<name>')
def f(name):
    return name

@app.route('/hello')
def hello():
    return 'Hello page'

