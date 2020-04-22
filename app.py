from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index page'

@app.route('/<name>')
def f(name):
    return hello(name)

@app.route('/hello')
def hello(name='new user'):
    return render_template('hello.html', name=name)

@app.route('/hello/')
def about():
    return 'The about page'
