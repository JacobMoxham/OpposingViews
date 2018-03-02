from pymongo import MongoClient


class FeedbackDB():
    def __init__(self):
        client = MongoClient()
        self.db = client['feedback']

    def store_feedback(self, feedback, from_url, to_url):
        # create link
        feedback_link = {
            'feedback': feedback,
            'from': from_url,
            'to': to_url
        }
        # store in db
        feedback_links = self.db.feedback_links
        feedback_links.insert_one(feedback_link)

    def count_pos(self, url, links=None):

        if links is None:
            # find documents terminating at passed url
            links = self.db.find({'to': url})

        # initialise count
        pos = 0
        # count positive feedback
        for l in links:
            if l['feedback'] == 'positive':
                pos += 1

        return pos

    def count_neg(self, url, links=None):

        if links is None:
            # find documents terminating at passed url
            links = self.db.find({'to': url})

        # initialise count
        neg = 0
        # count positive feedback
        for l in links:
            if l['feedback'] == 'negative':
                neg += 1

        return neg

    def percentage_positive(self, url, links = None):

        if links is None:
            # find documents terminating at passed url
            links = self.db.find({'to': url})

        pos = self.count_pos(url, links)
        neg = self.count_neg(url, links)

        # TODO: check this is not int
        return pos / neg
