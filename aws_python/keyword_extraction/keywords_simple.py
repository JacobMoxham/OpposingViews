from keyword_extraction.tfidf import tfidf
import json

with open('reuters_idf.json') as f:
    FREQS = json.load(f)

def keywords(title, text, n=5, title_multiplier=2, threshold_count=4, ignore_punctuation=True):
    """
    Extract top `n` keywords from text using tfidf (proper nmf will be implemented later)

    """

    keyword = tfidf(text, FREQS).most_common(n)

    return [k[0] for k in keyword]
