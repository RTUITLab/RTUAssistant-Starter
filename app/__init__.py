from flask import Flask

app = Flask(__name__)

import sounddevice as sd
import numpy as np
import tensorflow as tf
import scipy as sp
import scipy.signal
import time

from app import views


def norm(x):
    std = np.std(x ,ddof=1)
    return (x - np.mean(x)) / std

def func(_x, _sr=44100):
    _x = np.reshape(_x, len(_x))
    _x = tf.keras.preprocessing.sequence.pad_sequences(
        [_x],
        maxlen=int(_sr * 0.4),
        padding='post',
        truncating='post',
        dtype='float32'
    )[0]
    coeff = sp.signal.firwin(999, [260, 700], fs=_sr, pass_zero=False)
    x_filtered = sp.signal.lfilter(coeff, 1.0, _x)
    x_normalized = x_filtered/x_filtered.max()
    x_squared = np.square(x_normalized)
    splited = np.array_split(x_squared, 20)
    e_parts = np.empty((0))
    for part in splited:
        e_parts = np.append(e_parts, sp.integrate.simps(part))
    return np.reshape(norm(e_parts), (1, 1, 20))


sd.default.samplerate = 44100
sd.default.channels = 1

rec_duration = 0.1

count = 0
prediction = 0

k = 0
tmp_count = 0

model = tf.keras.models.load_model(r"app\Mira_GRU-v1.0.h5", compile=False)

names = {
    0 : 'None',
    1 : 'Mira',
}

data = sd.rec(int(4 * 0.1 * sd.default.samplerate), blocking=True)

name = 'None'

def callback(indata, outdata, frames, time, status):
    #outdata[:] = indata
    global name, model, data, count, prediction, k, tmp_count
    
    k += 1
    data = data[frames:]
    data = np.append(data, indata, axis=0)
    prediction = model(func(data))[0][1]
    class_id = int(prediction > 0.65)
    tmp_count += class_id
    name = names[class_id]
    if k == 4:
        k = 0
        if tmp_count > 0:
            count += 1
            sd.play(data)
        tmp_count = 0
    
    
block = int(sd.default.samplerate * rec_duration)
stream = sd.Stream(blocksize=block, callback=callback)
start_time = stream.time
