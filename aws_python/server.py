#!/usr/bin/env python3

from global_config import USE_CACHING
from global_config import STORE_FEEDBACK
from mongo_heuristics.database_access import HeuristicsDB
from mongo_feedback.database_access import FeedbackDB
import pipeline
import json
import time
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado import gen


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.write("Hello, world")


class GetViewsHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        start = time.time()
        if USE_CACHING:
            heur_db = HeuristicsDB()
        else:
            heur_db = None
        url = self.get_argument('link', '')
        res = json.dumps(pipeline.pipeline_test(db=heur_db, passed_url=url))
        if heur_db is not None:
            heur_db.close()
        end = time.time()
        logging.info("Time of running pipeline was "
                     + str(end - start)
                     + " seconds"
                     )
        self.write(res)


class FeedbackHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        print('received POST request')
        to_site = self.get_argument('toSite', '')
        from_site = self.get_argument('fromSite', '')
        feedback = self.get_argument('feedback', '')

        # store feedback in the database if flag is set
        # this format is maintained so we can hopefully easily move this so we only open a connection once
        if STORE_FEEDBACK:
            feedback_db = FeedbackDB()
        else:
            feedback_db = None

        if STORE_FEEDBACK:
            print('Store:', from_site, to_site, feedback)
            feedback_db.store_feedback(feedback, from_site, to_site)

        if feedback_db is not None:
            feedback_db.close()

        self.write(json.dumps({
            'message': 'From site : ' + from_site +
                       ' \n To site : ' + to_site +
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
    # server.bind(8080)
    # server.start(0)
    tornado.ioloop.IOLoop.current().start()
