#!/usr/bin/env python3

from global_config import USE_CACHING
from global_config import STORE_FEEDBACK
from mongo_heuristics.database_access import HeuristicsDB
from mongo_feedback.database_access import FeedbackDB
import bottle
from bottle import Bottle, route, request, run
import pipeline
import json
import time

app = bottle.app()

heur_db = None
if USE_CACHING:
    print("Using caching - connecting to db...")
    heur_db = HeuristicsDB()

feedback_db = None
if STORE_FEEDBACK:
    print("Storing feedback - connecting to db...")
    feedback_db = FeedbackDB()


@app.route('/')
def success():
    return "I'm working!"


@app.route('/get-views', method='POST')
def handle_event():
    request_time = time.time()
    url = request.forms.get('link')
    res = pipeline.pipeline_test(db=heur_db, passed_url=url)
    json_res = json.dumps(res)
    response_time = time.time()
    print("Total time of processing: " +
          str(response_time - request_time) +
          " seconds")
    return json_res


@app.route('/feedback-processing', method='POST')
def handle_feedback():
    to_site = request.forms.get('toSite')
    from_site = request.forms.get('fromSite')
    feedback = request.forms.get('feedback')
    if STORE_FEEDBACK:
        feedback_db.store_feedback(feedback, from_site, to_site)
    return json.dumps({'message': 'From site : ' + from_site + ' \n To site : ' + to_site + '\n Feedback: ' + feedback})


run(app, host='0.0.0.0', port='8080')
