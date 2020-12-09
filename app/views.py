from app import app
from app import RECORDER
from flask import render_template, jsonify


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/req', methods=['GET'])
def req():
    return jsonify({
        'time': str(int(RECORDER.STREAM.time-RECORDER.START_TIME)),
        'name': "Mira" if RECORDER.PREDICTOR.class_id else 'None',
        'count': RECORDER.COUNT,
        'prediction': str(RECORDER.PREDICTOR.prediction),
    })

@app.route('/stop', methods=['POST'])
def stop():
    RECORDER.STREAM.stop()
    return jsonify({'success' : 1})

@app.route('/start', methods=['POST'])
def start():
    RECORDER.STREAM.start()
    return jsonify({'success' : 1})
