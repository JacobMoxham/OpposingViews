from goose3 import Goose

def extract_content(url):
    g = Goose({'enable_image_fetching': True})
    article = g.extract(url=url)
    return article
