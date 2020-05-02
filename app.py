from flask import Flask, render_template, redirect
import sounddevice as sd
import numpy as np
import time

app = Flask(__name__)

sd.default.samplerate = 44100
sd.default.channels = 1

rec_duration = 0.1
start_duration = 0.5

i = 0

@app.route('/')
def index(time=''):
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
    
block = int(sd.default.samplerate * rec_duration)
stream = sd.Stream(blocksize=block, callback=callback)
start_time = stream.time


