from pymongo import MongoClient


class HeuristicsDB:
    def __init__(self):
        self.client = MongoClient()

        # test connection
        self.client.server_info()

        # store heuristics DB
        self.db = self.client['article_heuristic_scores']

    def close(self):
        self.client.close()

    '''
    Parameters
    ----------
    db : database
        the database mapping articles to precomputed dictionaries of heuristics
    url : string
        the url of the article to store
    heuristics : dict
        the dictionary of heuristic names and values between 0 and 1 for the article
    Return
    ------
    result : InsertOneResult
        the result of inserting the document
    '''

    def write_article(self, url, heuristics, content_hash=""):
        # We do not specify url as _id here as we may end up with more than one entry
        # over time for the same id. This problem is ignored later via the use of find_one
        # but the solution at least remains robust.
        article = {
            "url": url,
            "heuristics": heuristics,
            "content_hash": content_hash
        }
        articles = self.db.articles
        # Return the result
        return articles.insert_one(article)

    # TODO: implement this when we know what the articles look like in the rest of the system
    # def write_articles(db, articles):


    '''
    Parameters
    ----------
    db : database
        the database mapping articles to precomputed dictionaries of heuristics
    url : string
        the url of the article to look up
    Return
    ------
    heuristics : dict
        the dictionary of heuristic names and values between 0 and 1 of the article
        stored for the requested url or None if it did not have an entry
    '''

    def read_article(self, url):
        articles = self.db.articles
        return articles.find_one({"url": url})
