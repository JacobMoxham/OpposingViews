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

        feedback_links = self.db.feedback_links

        if feedback != 'click':
            # check db for 'click' entry
            feedback_link = feedback_links.find({'from': from_url, 'to': to_url})

        if feedback_link is None:
            # create link
            feedback_link = {
                'feedback': feedback,
                'from': from_url,
                'to': to_url
            }
        else:
            # just update the feedback
            feedback_link['feedback'] = feedback

        # store in db
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

    def percentage_positive(self, url, links = None):

        if links is None:
            # find documents terminating at passed url
            links = self.db.feedback_links.find({'to': url})

        pos = self.count_pos(url, links)

        # TODO: check this is not int
        if pos > 0:
            return pos / len(links)
        else:
            return 0
