import tensorflow as tf
import numpy as np
import scipy as sp
import scipy.signal


class Predictor():
    def __init__(self, path_to_model):
        with tf.device('CPU:0'):
            self.model = tf.keras.models.load_model(path_to_model)
            self.model.compile(
                optimizer=self.model.optimizer,
                loss=self.model.loss,
            )
        self.class_id = 0
        self.prediction = 0
        
    def predictions(self, data):
        predictions = []
        for parts in range(4000, 8001, 4000):
            e_parts = self.get_energy(data[parts:])
            with tf.device('CPU:0'):
                predictions.append(self.model(e_parts)[0][0].numpy())
        return predictions

    def get_energy(self, data, sr=16000):
        x = tf.keras.preprocessing.sequence.pad_sequences(
            [data],
            maxlen=int(16000 * 1.0),
            padding='post',
            truncating='post',
            dtype='float32'
        )[0]
        x = tf.reshape(x, (sr))
        coeff = sp.signal.firwin(999, [260, 700], fs=sr, pass_zero=False)
        x_filtered = sp.signal.lfilter(coeff, 1.0, x)
        x_normalized = x_filtered / x_filtered.max()
        x_squared = np.square(x_normalized)
        splited = np.array_split(x_squared, 200)
        e_parts = np.empty((0))
        for part in splited:
            e_parts = np.append(e_parts, sp.integrate.simps(part))
        return np.reshape(e_parts, (1, 200))

    def predict(self, data, limit=0.5):
        preds = self.predictions(data)
        self.prediction = tf.math.reduce_mean(preds).numpy()
        self.class_id = int(self.prediction > limit)
