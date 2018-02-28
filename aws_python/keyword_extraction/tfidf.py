import numpy as np
from nltk.corpus import reuters
from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation
from collections import Counter
import json

# from goose3 import Goose

# url = 'http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2'


def tokenize(text):
    # tokenize + removal of stopwords and numbers
    stop_words = stopwords.words('english') + list(punctuation)
    words = word_tokenize(text.lower())
    return [w for w in words if w not in stop_words and not w.isdigit() and w.isalnum()]


def get_idf():
    vocabulary = set()
    for file_id in reuters.fileids():
        words = tokenize(reuters.raw(file_id))
        vocabulary.update(words)

    vocabulary = list(vocabulary)
    
    internal_word_index = {w: idx for idx, w in enumerate(vocabulary)}

    vocabulary_size = len(vocabulary)
    doc_count = len(reuters.fileids())

    word_idf = np.zeros(vocabulary_size)
    for file_id in reuters.fileids():
        words = set(tokenize(reuters.raw(file_id)))
        indexes = [internal_word_index[word] for word in words]
        word_idf[indexes] += 1.0

    # return np.log(doc_count / (1 + word_idf).astype(float)), internal_word_index

    word_idf = np.log(doc_count / (1 + word_idf).astype(float))

    idf_dict = {}
    for i in range(len(vocabulary)):
        idf_dict[vocabulary[i]] = word_idf[i]

    with open('reuters_idf.json', 'w') as f:
        json.dump(idf_dict, f)


def tfidf(text, word_idf):
    text = tokenize(text)
    length = len(text)
    tfidf = Counter(text)

    for key in tfidf:
        if key not in word_idf:
            tfidf[key] = float(tfidf[key]) * 13 / length
        else:
            tfidf[key] = float(tfidf[key]) * word_idf[key] / length

    return tfidf


def tfidf_weighted(text, word_idf):
    text = tokenize(text)
    length = len(text)

    start = text[0:100]
    middle = text[100:length-100]
    end = text[length-100:length-1]

    tfidf1 = Counter(start)
    tfidf2 = Counter(middle)
    tfidf3 = Counter(end)

    for key in tfidf1:
        if key not in word_idf:
            tfidf1[key] = float(tfidf1[key]) * 13 / len(start)
        else:
            tfidf1[key] = float(tfidf1[key]) * word_idf[key] / len(start)

    for key in tfidf2:
        if key not in word_idf:
            tfidf2[key] = float(tfidf2[key]) * 13 / len(middle)
        else:
            tfidf2[key] = float(tfidf2[key]) * word_idf[key] / len(middle)

    for key in tfidf3:
        if key not in word_idf:
            tfidf3[key] = float(tfidf3[key]) * 13 / len(end)
        else:
            tfidf3[key] = float(tfidf3[key]) * word_idf[key] / len(end)

        tfidf3[key] = (tfidf3[key] + tfidf2[key] + tfidf1[key]) / 3.0

    return tfidf3


# g = Goose()

# idf, iwi = get_idf()
# article = g.extract(url=url)
# t = tfidf_weighted(article.cleaned_text, idf, iwi)
# print(t.most_common(10))
