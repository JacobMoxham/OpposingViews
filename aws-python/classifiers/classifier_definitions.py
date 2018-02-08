"""
Contains function definitions that are needed by both training.py and classifiers.py.
"""
import re


def preprocess(string):
    """
    Replace words in quotes with those words followed by INQUOTES, and remove words that are directly linked to sources.
    """
    def replace(obj):
        return re.sub(r'\b(\w\w+)\b', r'\1INQUOTES', obj.group())

    string = string.lower()
    string = re.sub(r'"([^"]*)"', replace, string)

    # replace informative features that are too tightly coupled to sources
    bad_words = ['npr', 'breitbart', 'guardian', 'fox', 'foxnews', 'facebooksharetweet', 'follow', 'com', 'pic', 'twitter', 'https',]
    for w in bad_words:
        string = string.replace(w, '')

    return string
