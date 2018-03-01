#!/usr/bin/env python3

from global_config import USE_CACHING
from mongo.database_access import HeuristicsDB
import pipeline
import json
import time
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado import gen

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class GetViewsHandler(tornado.web.RequestHandler):
    def post(self):
        start = time.time()
        if USE_CACHING:
            db = HeuristicsDB()
        else:
            db = None
        url = self.get_argument('link','')
        res = json.dumps(pipeline.pipeline_test(db=db, passed_url=url))
        if db is not None:
            db.close()
        end = time.time()
        logging.info("Time of running pipeline was "
                + str(end - start)
                + " seconds"
                )
        self.write(res)

class FeedbackHandler(tornado.web.RequestHandler):
    def post(self):
        toSite = self.get_argument('toSite', '')
        fromSite = self.get_argument('fromSite', '')
        feedback = self.get_argument('feedback', '')
        self.write(json.dumps({
                'message': 'From site : ' + fromSite + 
                            ' \n To site : ' + toSite + 
                            '\n Feedback: ' + feedback
                }))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/get-views", GetViewsHandler),
        (r"/feedback-processing", FeedbackHandler),
    ])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    print("Server loaded and running...")
    server.listen(8080)
    #server.bind(8080)
    #server.start(0)
    tornado.ioloop.IOLoop.current().start()
