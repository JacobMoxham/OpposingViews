from keyword_extraction.keywords_rlms import keywords as k_r
from keyword_extraction.keywords_simple import keywords as k_s
from keyword_extraction.keywords_weighted import keywords as k_w
# from keywords_metadata import keywords as k_m


def keywords(title, text, idf, iwi, n=5, ipl=1):
    """
    Runs a keyword extraction implementation depending on passed arguments.
    """

    options = {1: k_r,
               2: k_s,
               3: k_w,
               # 4: sqr,
               }

    return options[ipl](title, text, idf, iwi, n)
