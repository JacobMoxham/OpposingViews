# TODO
import numpy as np
from math import log
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation
from collections import Counter

# from goose3 import Goose

# url = 'http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2'


def tokenize(words):
    # tokenize + removal of stopwords and numbers
    stop_words = stopwords.words('english') + list(punctuation)
    return [w.lower() for w in words if w not in stop_words and not w.isdigit() and w.isalnum()]


def get_newsprobs():
    all_words = Counter()

    for file_id in brown.fileids('editorial'):
        words = tokenize(brown.words(file_id))
        all_words.update(words)

    for file_id in brown.fileids('reviews'):
        words = tokenize(brown.words(file_id))
        all_words.update(words)

    news_words = Counter()

    for file_id in brown.fileids('news'):
        words = tokenize(brown.words(file_id))
        all_words.update(words)
        news_words.update(words)

    for key in all_words:
        if key not in news_words:
            all_words[key] = float(float(0.5) / float(all_words[key] + 1))
        else:
            all_words[key] = float(float(news_words[key] + 0.5) / float(all_words[key] + 1))

    return all_words


def oped_check(text, words):
    tokens = tokenize(text)
    vocab = words.keys()

    probnews = 0
    for token in tokens:
        if token not in vocab:
            probnews = probnews + log(0.5)
        else:
            probnews = probnews + log(words[token])


    proboped = 0
    for token in tokens:
        if token not in vocab:
            proboped = proboped + log(0.5)
        else:
            proboped = proboped + log(1 - words[token])

    print('Oped score:')
    print(proboped - probnews)
    print('Received Output')
    return proboped > probnews

