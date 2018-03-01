#!/usr/bin/env python3

from global_config import USE_CACHING
from mongo.database_access import HeuristicsDB
import bottle
from bottle import Bottle, route, request, run
import pipeline
import json
import time

app = bottle.app()

db = None
if USE_CACHING:
    print("Using caching - connecting to db...")
    db = HeuristicsDB()


@app.route('/')
def success():
    return "I'm working!"


@app.route('/get-views', method='POST')
def handle_event():
    request_time = time.time()
    url = request.forms.get('link')
    res = pipeline.pipeline_test(db=db, passed_url=url)
    json_res = json.dumps(res)
    response_time = time.time()
    print("Total time of processing: " +
            str(response_time - request_time) +
            " seconds")
    return json_res


@app.route('/feedback-processing', method='POST')
def handle_feedback():
    toSite = request.forms.get('toSite')
    fromSite = request.forms.get('fromSite')
    feedback = request.forms.get('feedback')
    return json.dumps({'message': 'From site : ' + fromSite + ' \n To site : ' + toSite + '\n Feedback: ' + feedback})


run(app, host='0.0.0.0', port='8080')
