from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation


def hasnum(s):
    return any(c.isdigit() for c in s)


def get_names(words):
    caps = set([w for w in words if len(w) > 1 and w[0].isupper() and not w[1].isupper()])
    names = []
    for c in caps:
        if not c.lower() in words:
            names.append(c)
    return names


def filter_tokens(words):
    # tokenize + removal of stopwords and numbers
    words = [w.lower() for w in words]
    stop_words = stopwords.words('english') + list(punctuation) + ['mr', 'dr', 'mrs']
    return [w for w in words if w not in stop_words and not hasnum(w) and w.isalnum()]


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

    new_keywords = []
    old_keywords = []
    for k in keywords:
        if k in names and k not in title_tokens:
            old_keywords.append(k)
        else:
            new_keywords.append(k)

    return new_keywords, old_keywords
