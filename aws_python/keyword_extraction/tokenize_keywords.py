from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation


def hasnum(s):
    return any(c.isdigit() for c in s)


def get_names(words):
    return [x[0].isupper() in words]


def filter_tokens(words):
    # tokenize + removal of stopwords and numbers
    stop_words = stopwords.words('english') + list(punctuation)
    return [w.lower() for w in words if w not in stop_words and not hasnum(w) and w.isalnum()]


def tokenize(text):
    return word_tokenize(text)


def post_tokenize(keywords):
    for k in keywords:
        if len(k) > 3:
            first = False
            for l in keywords:
                if l.startswith(k):
                    if first:
                        keywords.remove(l)
                    else:
                        keywords[keywords.index(l)] = k
                        first = True

    for k in keywords:
        if len(k) > 3 and k.endswith('s'):
            stm = k[:-1]
            first = False
            for l in keywords:
                if l.startswith(stm):
                    if first:
                        keywords.remove(l)
                    else:
                        first = True
    return keywords


def filter_names(title, text, keywords):
    names = [w.lower() for w in get_names(text)]
    title_tokens = filter_tokens(title)

    for k in keywords:
        if k in names and k not in title_tokens:
            keywords.remove(k)

    return keywords
