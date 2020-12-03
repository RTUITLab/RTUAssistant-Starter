from flask import Flask

from app.recorder import Recorder

RECORDER = None
RECORDER = Recorder(r'app\Mira_GRU-v4.1.h5')
RECORDER.listen()

app = Flask(__name__)

from app import views
