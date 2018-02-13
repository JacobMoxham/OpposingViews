from .backend import SimlarArticleBackend
import urllib.parse
import feedparser

BASE_URL = "https://news.google.com/news/rss/explore/section/q/"


class BackendGoogle(SimlarArticleBackend):
    def __init__(self):
        self.backend_name = "Google RSS Feed"

    def get_similar_for_keywords(self, keywords):
        return self.get_similar_for_topic(" ".join(keywords))

    def _generate_url(self, topic):
        return "{:s}{:s}".format(BASE_URL, urllib.parse.quote(topic, safe=''))

    def get_similar_for_topic(self, topic):
        d = feedparser.parse(self._generate_url(topic))
        return [{'title': e['title'], 'url': e['link']} for e in d.entries]

    def list_topic(self, topic):
        entries = self.get_similar_for_topic(topic)
        print("Got {:d} entries".format(len(entries)))
        for e in entries:
            print("\"{:s}\" - {:s}".format(e['title'], e['url']))
