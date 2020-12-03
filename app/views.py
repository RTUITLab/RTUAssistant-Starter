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
        'name': RECORDER.PREDICTOR.class_id,
        'count': RECORDER.COUNT,
        'prediction': 'None',
    })

@app.route('/stop', methods=['POST'])
def stop():
    RECORDER.STREAM.stop()
    #APP.count = 0
    return jsonify({'success' : 1})

@app.route('/start', methods=['POST'])
def start():
    RECORDER.STREAM.start()
    return jsonify({'success' : 1})
