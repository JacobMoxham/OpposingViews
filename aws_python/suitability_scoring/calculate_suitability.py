
# Weights of heuristics
# TODO: tune weights (@Jacob Moxham)
# TODO: Add type of publication - non-numeric so how to handle?
weights = {'sentiment': 1.0, 'source_politics': 1.0, 'opinion_strength': 1.0, 'seriousness': 1.0}

'''
Parameters
----------
article_heuristics : dict
    contains a number between 0 and 1 for each used heuristics for the initial article
comparison_heuristics : dict
    contains a number between 0 and 1 for each used heuristics for the similar article
heuristics : list
    contains the used heuristics
    
Return
------
suitability : double
    the weighted average in differences for the heuristics
'''
def calculate_suitability(article_heuristics, comparison_heuristics, heuristics):
    suitability = 0
    # normalize weights
    normalized_weights = {}
    # get weights total
    total_weights = 0
    for h in heuristics:
        if h in weights:
            total_weights += weights[h]
        else:
            total_weights += 1.0

    # calculate normalized weights by dividing by total
    for h in heuristics:
        if h in weights:
            normalized_weights[h] = weights[h] / total_weights
        else:
            normalized_weights[h] = 1.0/total_weights

    # Sum heuristics using weights
    for h in heuristics:
        # calculate abs difference between each heuristic for the original and similar article
        difference = abs(article_heuristics[h] - comparison_heuristics[h])
        # get weight, checking it exists
        weight = normalized_weights[h]
        # add weighted difference to suitability
        suitability += weight*difference

    # return the weighted average of the differences
    return suitability


'''
Parameters
----------
initial_article_heuristics : dict
    contains a number between 0 and 1 for each used heuristics for the initial article
    
comparison_articles_and_heuristics : list (article,dict)
    contains a list of articles and dict of numbers between 0 and 1 for each used heuristics for the similar article

Return
------
suitable_articles : list articles
    list of artciles and suitabilities sorted by the weighted average in differences for the 
    intersection of initial and comparison heuristics
'''
def get_suitable_articles(initial_article_heuristics, comparison_articles_and_heuristics):
    suitable_articles = []

    initial_heurs = set(initial_article_heuristics.keys())
    # iterate over articles to compare with
    for article, article_heuristics in comparison_articles_and_heuristics:
        # get heuristics we can use for this article
        comp_heurs = set(article_heuristics.keys())
        heurs_intersection = initial_heurs.intersection(comp_heurs)

        # get suitability
        suitability = calculate_suitability(initial_article_heuristics, article_heuristics, heurs_intersection)
        # TODO: add a minimum cut off
        suitable_articles.append((article, suitability))

    # sort articles by suitability in descending order
    suitable_articles.sort(key = lambda x: x[1], reverse = True)
    # return sorted list
    return suitable_articles
