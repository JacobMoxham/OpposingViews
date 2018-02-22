from keyword_extraction.tfidf import tfidf_weighted


def keywords(title, text, idf, iwi, n=5):
    """
    Extract top `n` keywords from text using tfidf and weighting term frequencies with the part of the text
    it came from.
    The first 100 words and last 100 words are weighted the same as the middle body of text.
    Will implement title weighting as well later.
    """

    keyword = tfidf_weighted(text, idf, iwi).most_common(n)

    return [k[0] for k in keyword]
