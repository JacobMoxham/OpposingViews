from keyword_extraction.keywords_rlms import keywords as k_r
from keyword_extraction.keywords_simple import keywords as k_s
from keyword_extraction.keywords_weighted import keywords as k_w
from keyword_extraction.tokenize_keywords import tokenize, post_tokenize, filter_names
from content_extraction.proper_nouns.extract_proper_nouns import ExtractProperNouns

def k_union(title, text, n):
    r = k_r(title, text, n)
    s = k_s(title, text, n)
    w = k_w(title, text, n)
    union = []
    for x in range(0, n):
        if len(w) > x:
            union.append(w[x])
        if len(s) > x:
            union.append(s[x])
        if len(r) > x:
            union.append(r[x])

    new, old = filter_names(title, text, sorted(set(union), key=lambda x: union.index(x)))

    if len(new) < n:
        new.extend(old)
        return new[:n]

    return new[:n + 1]


def k_proper_nouns(title, text, rawtext, n):
    return list(set(k_union(title, text, n)).union(ExtractProperNouns().extract_proper_nouns(rawtext)))


options = [
    k_union,
    k_r,
    k_s,
    k_w,
    ]


def keywords(title, text, ipl=0, n=5):
    """
    Runs a keyword extraction implementation depending on passed arguments.
    """

    if ipl == 4:
        return k_proper_nouns(tokenize(title), tokenize(text), text, n)

    return options[ipl](tokenize(title), tokenize(text), n)
