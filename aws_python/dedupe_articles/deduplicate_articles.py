from .hash_functions import compare_similarities


def get_unique_hashes(possible_dupes, extra_articles=None):
    if extra_articles is None:
        extra_articles = []

    seen_hashes = extra_articles.copy()
    output = []

    for test_hash in possible_dupes:
        is_unique = True

        for other_hash in seen_hashes:
            if compare_similarities(test_hash, other_hash) > 0.2:
                is_unique = False
                break

        output.append(1 if is_unique else 0)
        seen_hashes.append(test_hash)

    return output
