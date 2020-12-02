import sounddevice as sd
import numpy as np
from .predictor import Predictor
from app import app


sd.default.samplerate = 44100
sd.default.channels = 1

REC_DURATION = 0.1
STREAM = None
START_TIME = None
PREDICTOR = None

def listen():

    def callback(indata, outdata, frames, time, status):
        global data
        #outdata[:] = indata
        data = data[frames:]
        data = np.append(data, indata, axis=0)
        PREDICTOR.predict(data)

    PREDICTOR = Predictor(r"app\Mira_GRU-v1.0.h5")
    data = sd.rec(int(1.0 * sd.default.samplerate), blocking=False)
    block = int(sd.default.samplerate * REC_DURATION)
    STREAM = sd.Stream(blocksize=block, callback=callback)
    START_TIME = STREAM.time


def get_default_devices():
    devices = sd.query_devices()
    def_devices = sd.default.device
    devicesDict = dict()
    devicesDict['status'] = True
    try:
        devicesDict['input'] = devices[def_devices[0]]['name']
        devicesDict['output'] = devices[def_devices[1]]['name']
    except Exception as e:
        devicesDict['status'] = False
        devicesDict['exception'] = e
    return devicesDict


if __name__ == "__main__":
    pass