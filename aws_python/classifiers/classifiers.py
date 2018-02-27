"""
Load pre-trained classifiers from a file and expose an API to use them.

Classifiers can be created using scripts in the classifier_training directory.
"""
import sys
import logging

import numpy as np
from sklearn.externals import joblib

from .classifier_definitions import preprocess    # noqa: F401 (for flake8 linter)

# by default, classifer names are '<heuristic>_clf.pkl', CLASSIFER_FILENAMES contains any that don't follow that pattern
CLASSIFIER_FILENAMES = {}

try:
    politics = joblib.load('politics_clf.pkl')
    tone = joblib.load('classifiers/tone_clf.pkl')
except FileNotFoundError as e:
    logging.error("Could not locate classifier '{}'".format(e.filename))
    sys.exit()


def classify_list(articles):
    """
    Takes some dicts representing articles and returns a list of dicts of features.

    Input elements should have keys 'text', 'title', 'author', 'image' and 'source' (although currently only 'text' is used).
    Returns dicts with key 'source_politics', with value 0.0 for left-wing sources and 1.0 for right-wing ones.
    """
    texts = np.array([a['text'] for a in articles])
    politicses = politics.predict(texts)
    tones = tone.predict_proba(texts)

    result = []
    for i in range(len(texts)):
        p = politicses[i]
        t = tones[i][0] #Represents probability of neutrality
        result.append({'source_politics' : p, 'source_tone' : t})
    return result


def classify(article):
    """
    Helper function to classify an individual article.
    """
    return classify_list([article])[0]
