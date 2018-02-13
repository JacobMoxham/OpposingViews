from .backend import SimlarArticleBackend
import urllib.parse
import feedparser
import sys

BASE_URL = "https://news.google.com/news/rss/explore/section/q/"


class BackendGoogle(SimlarArticleBackend):
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


if __name__ == '__main__':
    backend = BackendGoogle()
    while True:
        print(">", end='')
        for line in sys.stdin:
            line = line.strip()
            print("Searching {:s}...".format(line))
            backend.list_topic(line)
            print("\n\n>", end='')