import matplotlib.pyplot as plt
import numpy as np
from urllib.parse import urlsplit
from aws_python.mongo_heuristics.database_access import HeuristicsDB
from content_extraction.extract_content import extract_content
from classifiers.classifiers import classify


def get_all_urls(db):
    links = db.get_all_links()
    urls = []
    for l in links:
        urls.append(l['to'])

    return urls


def plot_pos_percentages(db, urls=None):
    if urls is None:
        urls = get_all_urls(db)

    percentages = []
    for url in urls:
        percentages.append(db.percentage_positive(url))

    plt.clf()

    plt.hist(percentages, bins=[x / 10 for x in range(11)])
    plt.title('Positivity of feedback for articles in bins of size 0.1')
    plt.xlabel('Proportions of positive feedback')
    plt.ylabel('Number of articles')
    plt.savefig('../analysis_graphs/article_positivity.png')


def plot_liked_alternate_or_same_political_leaning(db, heur_db=None):
    if heur_db is None:
        heur_db = HeuristicsDB()

    # initialise counts
    left_left_pos = 0
    left_left_neg = 0
    left_right_pos = 0
    left_right_neg = 0
    right_left_pos = 0
    right_left_neg = 0
    right_right_pos = 0
    right_right_neg = 0

    links = db.get_all_links()

    # count for each type of connection
    for l in links:
        from_pol = heur_db.read_article(l['from'])['heuristics']['source_politics']
        to_pol = heur_db.read_article(l['to'])['heuristics']['source_politics']
        if l['feedback'] == 'positive':
            review = True
        elif l['feedback'] == 'negative':
            review = False
        else:
            # ignore 'click' links
            continue

        to_from_rev = (from_pol, to_pol, review)

        if to_from_rev == (0, 0, True):
            left_left_pos += 1
        elif to_from_rev == (0, 0, False):
            left_left_neg += 1
        elif to_from_rev == (1, 0, True):
            right_left_pos += 1
        elif to_from_rev == (1, 0, False):
            right_left_neg += 1
        elif to_from_rev == (0, 1, True):
            left_right_pos += 1
        elif to_from_rev == (0, 1, False):
            left_right_neg += 1
        elif to_from_rev == (1, 1, True):
            right_right_pos += 1
        elif to_from_rev == (1, 1, False):
            right_right_neg += 1
        else:
            print('plot_liked_alternate_or_same_political_leaning: malformed tuple')

    left_left = left_right_pos / (left_right_pos + left_left_neg) if left_right_pos > 0 else 0
    left_right = left_right_pos / (left_right_pos + left_right_neg) if left_right_pos > 0 else 0
    right_left = right_left_pos / (right_left_pos + right_left_neg) if right_left_pos > 0 else 0
    right_right = right_right_pos / (right_right_pos + right_right_neg) if right_right_pos > 0 else 0

    plt.clf()

    x = np.arange(4)
    plt.bar(x, [left_left, left_right, right_left, right_right])
    plt.xticks(x, ('left-left', 'left-right', 'right-left', 'right-right'))
    plt.ylim([0, 1])
    plt.xlabel('Political leanings of \'from\' articles and \'to\' articles')
    plt.ylabel('Proportion of positive feedback')
    plt.title('Positivity of feedback broken down by political leanings \n of the initial site and the suggested site')
    plt.savefig('../analysis_graphs/article_positivity_by_politics_to_and_from.png')


def plot_politics_per_site(urls, heur_db=None):
    if heur_db is None:
        heur_db = HeuristicsDB()

    urls_to_counts = {}
    for url in urls:
        article = extract_content(url)
        entry = heur_db.read_article(url)
        if entry is None:
            heurs = classify(article)
        else:
            heurs = entry['heuristics']

        url_stripped = urlsplit(url).netloc

        if urls_to_counts.get(url_stripped) is None:
            urls_to_counts[url_stripped] = {'left': 0, 'right': 0}

        if heurs['source_politics'] == 0:
            urls_to_counts[url_stripped]['left'] += 1
        else:
            urls_to_counts[url_stripped]['right'] += 1

    unique_urls = urls_to_counts.keys()
    short_urls = [url.split('.')[1] for url in urls_to_counts.keys()]
    url_left_proportions = [urls_to_counts[url]['left'] / (urls_to_counts[url]['left'] +
                                                           urls_to_counts[url]['right']) for url in unique_urls]
    plt.clf()

    plt.bar(short_urls, url_left_proportions)
    plt.ylim([0,1])
    plt.xlabel('Sites')
    plt.xlabel('Proportion of left leaning articles')
    plt.title('Proportions of left leaning articles for various sites')
    plt.savefig('../analysis_graphs/per_site_politics.png')


def amount_of_user_feedback(db):
    links = db.get_all_links()
    feedback = 0
    clicked = 0
    for l in links:
        if l[feedback] == 'click':
            clicked+=1
        else:
            feedback += 1

    if clicked > 0:
        return clicked / (clicked + feedback)
    else:
        return 0
