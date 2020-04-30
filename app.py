from flask import Flask, render_template, request, redirect
import sounddevice as sd
import numpy as np
#from tensorflow import keras
import scipy as sp
import scipy.signal

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index(name='Hello world'):
    name = request.args.get('name')
    return render_template('main.html', name=name)

@app.route('/request')
def req():
    request.args.add('name', 'req')
    # request.args.add('home', '/')
    # url = request.args.get('home')
    return redirect('/')





