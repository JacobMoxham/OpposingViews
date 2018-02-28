#!/usr/bin/env python3

from content_extraction.extract_content import extract_content
from similar_articles.frontend import find_similar_articles
from classifiers.classifiers import classify
from suitability_scoring.calculate_suitability import get_suitable_articles
from dedupe_articles import get_unique_hashes, hash_dirty_text

import time


def test(event):
    return [{"link": "http://www.bbc.co.uk/news/uk-politics-42929071",
             "imageLink": "https://ichef.bbci.co.uk/news/320/cpsprodpb/AFA4/production/_99746944_gettyimages-531840456.jpg",
             "title": "Jacob Rees-Mogg says Treasury 'fiddling figures' on Brexit",
             "summary": "Prominent Brexiteer Jacob Rees-Mogg has said he believes Treasury officials are 'fiddling the figures' on Brexit."},
            {"link": "http://www.bbc.co.uk/sport/winter-olympics/42840632",
             "imageLink": "https://ichef.bbci.co.uk/onesport/cps/480/cpsprodpb/11BEF/production/_99778627_winters.jpg",
             "title": "Winter Olympics 2018: Doping ban, neutral Russians & Pyeongchang medal hopes",
             "summary": "What was the point of banning Russia from the Winter Olympics when 169 of their athletes are still being allowed to compete as neutrals? "}]


def pipeline_test(passed_url, db=None):
    print("Got article suggestions request for URL '{:s}'".format(passed_url))
    # TODO: Use proper logger
    start_time = time.time()

    # extract content of passed url
    article = extract_content(passed_url)
    extraction_time = time.time()
    print("Extracting content from article took " + str(extraction_time - start_time) + " seconds")

    article_keywords = article['keywords']
    print("Keywords: {:s}".format(", ".join(article_keywords)))

    # find similar articles based on keywords
    # format: [{'title':<title>, 'url':<url>}, ...]
    similar_articles = find_similar_articles(article_keywords)
    similar_article_time = time.time()
    print("Similar articles:\n\t{:s}".format("\n\t".join([a["title"] for a in similar_articles])))
    print("Finding", len(similar_articles),"similar articles took " + str(similar_article_time - extraction_time) + " seconds")

    article_db_entry = None
    if db is not None:
        # check for db entry for initial article
        # TODO: consider checking when we last ran heuristics
        article_db_entry = db.read_article(passed_url)

    if article_db_entry is None:
        # run heuristics on initial article
        initial_heuristics = classify({'text': article['text']})
        source_article_hash = hash_dirty_text(article['text'])
        if db is not None:
            # write to DB
            db.write_article(url=str(passed_url), heuristics=initial_heuristics, content_hash=source_article_hash)
    else:
        # use cached heuristics if possible
        initial_heuristics = article_db_entry['heuristics']
        source_article_hash = article_db_entry['content_hash']

    initial_heuristic_time = time.time()
    print("Got cached initial heuristics, took " + str(initial_heuristic_time - similar_article_time) + " seconds")

    # run heuristics on each similar article
    analysed_articles = []
    for entry in similar_articles:
        url = entry['url']

        try:
            cached_article = None
            if db is not None:
                # check if we have cached this article
                # TODO: consider checking when we last ran heuristics
                cached_article = db.read_article(url)

            # TODO: consider caching this info
            comparison_article = extract_content(url)
            have_updated_article_data = False

            if cached_article is None or cached_article['heuristics'] is None:
                comparison_heuristics = classify({'text': comparison_article['text']})
                have_updated_article_data = True
            else:
                comparison_heuristics = cached_article['heuristics']

            if cached_article is None or not cached_article['content_hash']:
                article_hash = hash_dirty_text(comparison_article['text'])
                have_updated_article_data = True
            else:
                article_hash = cached_article['content_hash']

            if have_updated_article_data and db is not None:
                db.write_article(url=url, heuristics=comparison_heuristics, content_hash=article_hash)

            # add article to list for suitability calculation
            analysed_articles.append(({'article': comparison_article, 'url': url, 'content_hash': article_hash}, comparison_heuristics))
        except Exception as e:
            print('Error extracting:', url)
            print('Error message:', e)
            print('\n')

    comparison_heuristic_time = time.time()
    print("Article fetching & running comparison heuristics took " + str(comparison_heuristic_time - initial_heuristic_time) + " seconds")

    # remove duplicates
    # article is unique is a list, s.t. article_is_unique[i] == 1 iff analysed_articles[i] is the first occurrence of an
    # article in the list
    article_is_unique = get_unique_hashes([a['content_hash'] for a, _ in analysed_articles], [source_article_hash])
    unique_analysed_articles = [aa for i, aa in enumerate(analysed_articles) if article_is_unique[i] is 1]
    print("Removed duplicate articles:\n\t{:s}".format("\n\t".join([a['url'] for i, (a, _) in enumerate(analysed_articles) if article_is_unique[i] is not 1])))
    duplicate_calculation_time = time.time()
    print("Removing duplicate articles took {:f} seconds".format(duplicate_calculation_time - comparison_heuristic_time))

    # run suitability calculations
    suitable_articles = get_suitable_articles(initial_heuristics, unique_analysed_articles)[:3]
    print("Suitable articles:\n\t{:s}".format("\n\t".join([a['article']['title'] for a,_ in suitable_articles])))
    suitability_calculation_time = time.time()
    print("Running suitability calculations took " + str(suitability_calculation_time - duplicate_calculation_time) + " seconds")

    # format for sending to plugin
    articles_to_return = []
    for suitable_article, _ in suitable_articles:
        suitable_article_attributes = suitable_article['article']
        ret_article = {"link": suitable_article_attributes['url'],
                       "imageLink": "",
                       "title": suitable_article_attributes['title'],
                       "summary": '%s%s' % (suitable_article_attributes['text'][:100], '...')
                       }
        articles_to_return.append(ret_article)

    # return 3 suitable articles
    return articles_to_return
