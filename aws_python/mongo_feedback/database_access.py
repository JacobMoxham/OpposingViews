from pymongo import MongoClient


class FeedbackDB():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['feedback']

    def close(self):
        self.client.close()

    def get_all_links(self):
        return self.db.feedback_links.find()

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
            links = self.db.feedback_links.find({'to': url})

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
            links = self.db.feedback_links.find({'to': url})

        # initialise count
        neg = 0
        # count positive feedback
        for l in links:
            if l['feedback'] == 'negative':
                neg += 1

        return neg

    def count_just_clicked(self, url, links=None):
        if links is None:
            # find documents terminating at passed url
            links = self.db.feedback_links.find({'to': url})

        # initialise count
        clicks = 0
        # count positive feedback
        for l in links:
            if l['feedback'] == 'click':
                clicks += 1

        return clicks

    def percentage_positive(self, url, links = None):

        if links is None:
            # find documents terminating at passed url
            links = self.db.feedback_links.find({'to': url})

        pos = self.count_pos(url, links)
        neg = self.count_neg(url, links)

        # TODO: check this is not int
        if pos > 0:
            return pos / (pos+neg)
        else:
            return 0
