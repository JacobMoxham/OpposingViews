from keyword_extraction.tfidf import tfidf_weighted
import json

with open('reuters_idf.json') as f:
    FREQS = json.load(f)

def keywords(title, text, n=5, title_multiplier=2, threshold_count=4, ignore_punctuation=True):
    """
    Extract top `n` keywords from text using tfidf and weighting term frequencies with the part of the text
    it came from.
    The first 100 words and last 100 words are weighted the same as the middle body of text.
    Will implement title weighting as well later.
    """

    keyword = tfidf_weighted(text, FREQS).most_common(n)

    return [k[0] for k in keyword]
