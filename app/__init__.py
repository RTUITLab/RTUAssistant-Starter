from flask import Flask

app = Flask(__name__)

from app import views
import recorder

if __name__ == "__main__":
    recorder.listen()
