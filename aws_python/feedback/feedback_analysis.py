import matplotlib.pyplot as plt

from aws_python.mongo_heuristics.database_access import HeuristicsDB


def get_all_urls(db):
    links = db.find({})
    urls = []
    for l in links:
        urls.append(l['url'])

    return urls


def plot_pos_percentages(db, urls=None):
    if urls is None:
        urls = get_all_urls(db)

    percentages = []
    for url in urls:
        percentages.append(db.percentage_positive(url))

    plt.plot(urls, percentages)
    plt.show()


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

    links = db.find({})

    # count for each type of connection
    for l in links:
        from_pol = heur_db.read_article(l['from'])['heuristics']['source_politics']
        to_pol = heur_db.read_article(l['to'])['heuristics']['source_politics']
        review = l['feedback'] == 'positive'

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

    left_left = left_right_pos/left_left_neg
    left_right = left_right_pos/left_right_neg
    right_left = right_left_pos/right_left_neg
    right_right = right_right_pos/right_right_neg

    plt.bar([left_left, left_right, right_left, right_right])
    