from flask import Flask

from app.recorder import Recorder

RECORDER = None
RECORDER = Recorder(r'app\MiraGRUV4.3.2-1.h5')
RECORDER.listen()

app = Flask(__name__)

from app import views
