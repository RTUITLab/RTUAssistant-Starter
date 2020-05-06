from flask import Flask, render_template, request, redirect, make_response, url_for
import sounddevice as sd
import numpy as np
#from tensorflow import keras
import scipy as sp
import scipy.signal
import requests
import time

app = Flask(__name__)

sd.default.samplerate = 44100
sd.default.channels = 1

rec_duration = 0.1
start_duration = 0.5

i = 0

@app.route('/')
def index():
    return render_template('main.html', time=stream.time-start_time)

@app.route('/request')
def req():
    return render_template('main.html', time=stream.time-start_time)

@app.route('/stop')
def stop():
    stream.stop()
    return redirect('/')

@app.route('/start')
def start():
    stream.start()
    return redirect('/')

def callback(indata, outdata, frames, time, status):
    outdata[:] = indata
    
    global i
    if i == 3:
        redirect('/request')
    # params = dict(time=i)
    # resp = requests.post('http://localhost:5000', params=params)
    # redirect(resp.url)
    
block = int(sd.default.samplerate * rec_duration)
stream = sd.Stream(blocksize=block, callback=callback)
start_time = stream.time
