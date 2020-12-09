import sounddevice as sd
import numpy as np
from .predictor import Predictor


sd.default.samplerate = 16000
sd.default.channels = 1


class Recorder():
    def __init__(self, path):
        self.REC_DURATION = 0.5
        self.STREAM = None
        self.START_TIME = None
        self.PREDICTOR = Predictor(path)
        self.data = None
        self.COUNT = 0

    def callback(self, indata, outdata, frames, time, status):
        #outdata[:] = indata
        self.data = self.data[frames:]
        self.data = np.append(self.data, indata, axis=0)
        self.PREDICTOR.predict(self.data)
        self.COUNT += self.PREDICTOR.class_id
        self.PREDICTOR.class_id = 0

    def listen(self):
        self.data = sd.rec(int(1.0 * sd.default.samplerate), blocking=False)
        block = int(sd.default.samplerate * self.REC_DURATION)
        self.STREAM = sd.Stream(blocksize=block, callback=self.callback)
        # self.STREAM.start()
        self.START_TIME = self.STREAM.time


    def get_default_devices(self):
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