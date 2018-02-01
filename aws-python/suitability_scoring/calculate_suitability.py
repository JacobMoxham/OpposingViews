
# Weights of heuristics
# TODO: tune weights (@Jacob Moxham)
# TODO: Add type of publication - non-numeric so how to handle?
weights = {'sentiment': 1.0, 'source_politics': 1.0, 'opinion_strength': 1.0, 'seriousness': 1.0}

def calculate_suitability(article_heuristics, comparison_heuristics, heuristics):
    suitability = 0
    # Sum heuristics using weights
    for h in heuristics:
        # Calulate abs difference between each heuristic for the original and similar article
        difference = abs(article_heuristics[h] - comparison_heuristics[h])
        weight = weights[h]
        suitability += weight*difference

    return suitability
