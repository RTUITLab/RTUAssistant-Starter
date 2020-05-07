from flask import Flask

app = Flask(__name__)

import sounddevice as sd
import numpy as np
import tensorflow as tf
import scipy as sp
import scipy.signal
import requests
import time
from app import views


def func(_x, _sr=44100):
    _x = np.reshape(_x, len(_x))
    coeff = sp.signal.firwin(999, [260, 700], fs=_sr, pass_zero=False)
    x_filtered = sp.signal.lfilter(coeff, 1.0, _x)
    x_normalized = x_filtered/x_filtered.max()
    x_squared = np.square(x_normalized)
    splited = np.array_split(x_squared, 20)
    e_parts = np.empty((0))
    for part in splited:
        e_parts = np.append(e_parts, sp.integrate.simps(part))
    return tf.keras.utils.normalize(e_parts)


sd.default.samplerate = 44100
sd.default.channels = 1

rec_duration = 0.1
start_duration = 0.5

model = tf.keras.models.load_model('AudRec_L2_v1-2(69-60).h5')

names = {
    0 : 'Джарвис',
    1 : 'Дио',
    2 : 'Итан',
    3 : 'Лада',
    4 : 'Мира',
    5 : 'Привет'
}

data = sd.rec(int((start_duration + 0.1) * sd.default.samplerate), blocking=True)
print('first rec')

name = ''

def callback(indata, outdata, frames, time, status):
    #outdata[:] = indata
    global name, model, data
    name = names[model.predict_classes(func(data))[0]]
    data = data[frames:]
    data = np.append(data, indata, axis=0)
    
    
    
block = int(sd.default.samplerate * rec_duration)
stream = sd.Stream(blocksize=block, callback=callback)
start_time = stream.time

print('end init')