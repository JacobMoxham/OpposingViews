#!/usr/bin/env python3
from bottle import Bottle, route, request, run
import json

app = Bottle()

@app.route('/')
def success():
    return "The feedback processing is working!"

@app.route('/feedback-processing', method='POST')
def handle_feedback():
    toSite = request.forms.get('toSite')
    fromSite = request.forms.get('fromSite')
    feedback = request.forms.get('feedback')
    return json.dumps({'message' : 'From site : ' + fromSite + ' \n To site : ' + toSite + '\n Feedback: ' + feedback})

run(app, host='0.0.0.0', port='8081')
