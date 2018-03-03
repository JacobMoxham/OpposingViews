from keyword_extraction.keywords_rlms import keywords as k_r
from keyword_extraction.keywords_simple import keywords as k_s
from keyword_extraction.keywords_weighted import keywords as k_w
from keyword_extraction.tokenize_keywords import tokenize, post_tokenize, filter_names
# from keywords_metadata import keywords as k_m


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

    return filter_names(title, text, sorted(set(union), key=lambda x: union.index(x)))[:n+1]


def keywords(title, text, n=5, ipl=1):
    """
    Runs a keyword extraction implementation depending on passed arguments.
    """

    options = {
                1: k_union,
                2: k_r,
                3: k_s,
                4: k_w,
                # 5: sqr,
               }

    return options[ipl](tokenize(title), tokenize(text), n)
