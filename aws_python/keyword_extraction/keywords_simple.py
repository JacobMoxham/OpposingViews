from keyword_extraction.tfidf import tfidf


def keywords(title, text, idf, iwi, n=5):
    """
    Extract top `n` keywords from text using tfidf (proper nmf will be implemented later)

    """

    keyword = tfidf(text, idf, iwi).most_common(n)

    return [k[0] for k in keyword]
