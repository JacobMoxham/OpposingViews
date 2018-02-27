from keyword_extraction.keywords_rlms import keywords as k_r
from keyword_extraction.keywords_simple import keywords as k_s
from keyword_extraction.keywords_weighted import keywords as k_w
# from keywords_metadata import keywords as k_m


def k_union(title, text, n):
    return list(set().union(k_r(title, text, n), k_s(title, text, n), k_w(title, text, n)))


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

    return options[ipl](title, text, n)
