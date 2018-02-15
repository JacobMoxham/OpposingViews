from suitability_scoring import calculate_suitability as cs

# define test initial article heuristics
inital_heuristics1 = {'sentiment': 0.7, 'source_politics': 0.1, 'opinion_strength': 0.5, 'seriousness': 0.3}
# now minus a heuristic
inital_heuristics2 = {'sentiment': 0.7, 'source_politics': 0.1, 'opinion_strength': 0.5}


# define some test comparison heuristics
# like initial1
test_heuristics = [
    {'sentiment': 0.2, 'source_politics': 0.2, 'opinion_strength': 0.1, 'seriousness': 0.8},
    # subset of initials
    {'sentiment': 0.5, 'source_politics': 0.3},
    # superset of initial2
    {'sentiment': 0.9, 'source_politics': 0.2, 'opinion_strength': 0.3, 'seriousness': 0.8},
    # some heuristics initial has and some it doesn't
    {'sentiment': 0.9, 'source_politics': 0.2, 'seriousness': 0.8},
    # intersection is empty set with initial2
    {'seriousness': 0.8}
]

print("Single article suitability calculation: ", cs.calculate_suitability(inital_heuristics1, test_heuristics[0],
                               ['sentiment', 'source_politics', 'opinion_strength', 'seriousness']))
print("")

articles = []
i = 0
for test in test_heuristics:
    articles.append(("article" + str(i), test))
    i+=1

print("Muti article suitability calculation, all heuristics: ", cs.get_suitable_articles(inital_heuristics1, articles))
print("")
print("Muti article suitability calculation, no seriousness: ", cs.get_suitable_articles(inital_heuristics2, articles))