from app import app
import app as APP
from flask import render_template, request, redirect, make_response, url_for, jsonify

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/req', methods=['GET'])
def req():
    return jsonify({
        'time': str(int(APP.stream.time-APP.start_time)),
        'name': APP.name,
        'latency': APP.stream.latency
    })

@app.route('/stop')
def stop():
    APP.stream.stop()
    return redirect('/')

@app.route('/start')
def start():
    APP.stream.start()
    return redirect('/')


