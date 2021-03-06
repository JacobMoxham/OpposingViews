import json
from collections import Counter
from keyword_extraction.tokenize_keywords import filter_tokens


with open('brown_freqs.json') as f:
    BASE_FREQS = json.load(f)
    MIN_FREQ = min(BASE_FREQS.values())


def keywords(title, text, n=5, title_multiplier=2, threshold_count=4, ignore_punctuation=True):
    """
    Extract top `n` keywords from a string, performing add-one smoothing on words that don't appear in the Brown corpus.
    Ignore words that appear below `threshold_count`, which is modified by counting words which appear in the title
    multiple times.

    If keywords can't be extracted from the body, just take words from the title with the lowest frequencies in the
    Brown corpus.
    """
    tokens = filter_tokens(text)
    counts = Counter(tokens)
    for key in counts:
        title_counts = Counter(filter_tokens(title))
        counts[key] += title_counts[key] * title_multiplier

    freqs = {key: counts[key] / len(tokens) for key in counts if counts[key] >= threshold_count}
    if ignore_punctuation:
        freqs = {key: freqs[key] for key in freqs if key.isalnum()}
    # technically add-[minimum count in Brown corpus] rather than add-one smoothing
    relative = {key: freqs[key] / BASE_FREQS.get(key, MIN_FREQ) for key in freqs}
    ordered = sorted(list(relative.keys()), key=lambda x: relative[x], reverse=True)

    if len(ordered) >= n:
        return ordered[:n]
    # otherwise use the title
    else:
        ordered = sorted(filter_tokens(title), key=lambda w: BASE_FREQS.get(w, MIN_FREQ))
        return ordered[:n]
