import re
import ssdeep


# Given some text, tries to get a hash for just the wordy-content
def hash_dirty_text(text):
    # clean text
    text = re.sub(r'[\W_]+', '', text)

    # lowercase text
    text = text.lower()

    # ssdeep hash
    return ssdeep.hash(text)


# Given two hashes, returns a float. 0 means no match, 1 means almost certainly identical. 0.1 is probably a good
# threshold
def compare_similarities(hash1, hash2):
    return ssdeep.compare(hash1, hash2) / 100.0
