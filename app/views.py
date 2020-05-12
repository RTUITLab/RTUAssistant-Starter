from app import app
import app as APP
from flask import render_template, jsonify


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/req', methods=['GET'])
def req():
    return jsonify({
        'time': str(int(APP.stream.time-APP.start_time)),
        'name': APP.name,
        'count': APP.count,
        'prediction': int(APP.prediction * 100)
    })

@app.route('/stop', methods=['POST'])
def stop():
    APP.stream.stop()
    APP.count = 0
    return jsonify({'success' : 1})

@app.route('/start', methods=['POST'])
def start():
    APP.stream.start()
    return jsonify({'success' : 1})
