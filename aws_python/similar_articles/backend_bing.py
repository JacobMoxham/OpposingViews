from .backend import SimlarArticleBackend
import requests
import sys

subscription_key = "96d05359d76f4e758906539daeab939e"
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"


class BackendBing(SimlarArticleBackend):
    def list_topic(self, topic):
        entries = self.get_similar_for_topic(topic)
        print("Got {:d} entries".format(len(entries)))
        for e in entries:
            print("\"{:s}\" - {:s}".format(e['title'], e['url']))

    def get_similar_for_keywords(self, keywords):
        return self.get_similar_for_topic(" ".join(keywords))

    def get_similar_for_topic(self, topic):
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": topic}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        return [{'title':e['name'], 'url':e['url']} for e in search_results["value"]]


if __name__ == '__main__':
    backend = BackendBing()
    while True:
        print(">", end='')
        for line in sys.stdin:
            line = line.strip()
            print("Searching {:s}...".format(line))
            backend.list_topic(line)
            print("\n\n>", end='')
