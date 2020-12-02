import tensorflow as tf
import numpy as np
import scipy as sp


class Predictor():
    def __init__(self, path_to_model):
        self.model = tf.keras.models.load_model(path_to_model)
        self.class_id = None
        
    def norm(self, x):
        std = np.std(x ,ddof=1)
        return (x - np.mean(x)) / std

    def func(self, _x, _sr=44100):
        _x = np.reshape(_x, len(_x))
        _x = tf.keras.preprocessing.sequence.pad_sequences(
            [_x],
            maxlen=int(_sr * 1.0),
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
        return np.reshape(self.norm(e_parts), (1, 1, 20))

    def predict(self, data, limit=0.5):
        prediction = self.model(self.func(data))[0][1]
        self.class_id = int(prediction > limit)
