import json
from collections import Counter

from nltk.corpus import brown

if __name__ == '__main__':
    counts = Counter(map(lambda x: x.lower(), brown.words()))
    length = len(brown.words())
    result = {key: counts[key] / length for key in counts}
    with open('brown_freqs.json', 'w') as f:
        json.dump(result, f)
