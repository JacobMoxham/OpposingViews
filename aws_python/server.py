#!/usr/bin/env python3
from bottle import Bottle, route, request, run
import pipeline
import json

app = Bottle()

@app.route('/')
def success():
    return "I'm working!"

@app.route('/get-views', method='POST')
def handle_event():
    url = request.forms.get('link')
    print(url)
    res = pipeline.pipeline_test(url)
    print(res)
    return json.dumps(res)

run(app, host='localhost', port='8080')
