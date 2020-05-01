from flask import Flask, render_template, request, redirect, make_response
import sounddevice as sd
import numpy as np
#from tensorflow import keras
import scipy as sp
import scipy.signal

app = Flask(__name__)

sd.default.samplerate = 44100
sd.default.channels = 1

rec_duration = 0.1
start_duration = 0.5

i = 0

@app.route('/')
@app.route('/index')
def index(time=0):
    return render_template('main.html', time=time)

@app.route('/request')
def req():
    global i
    i += 1
    return index(i)

def callback(indata, outdata, frames, time, status):
    
    outdata[:] = indata
    #return index()

block = int(sd.default.samplerate * rec_duration)
stream = sd.Stream(blocksize=block, callback=callback)
stream.start()


