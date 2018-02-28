#!/usr/bin/env python3

from global_config import USE_CACHING
from content_extraction.extract_content import extract_content
from similar_articles.frontend import find_similar_articles
from classifiers.classifiers import classify
from suitability_scoring.calculate_suitability import get_suitable_articles
from mongo.database_access import HeuristicsDB

import time
import urllib


def test(event):
    return [{"link": "http://www.bbc.co.uk/news/uk-politics-42929071",
             "imageLink": "https://ichef.bbci.co.uk/news/320/cpsprodpb/AFA4/production/_99746944_gettyimages-531840456.jpg",
             "title": "Jacob Rees-Mogg says Treasury 'fiddling figures' on Brexit",
             "summary": "Prominent Brexiteer Jacob Rees-Mogg has said he believes Treasury officials are 'fiddling the figures' on Brexit."},
            {"link": "http://www.bbc.co.uk/sport/winter-olympics/42840632",
             "imageLink": "https://ichef.bbci.co.uk/onesport/cps/480/cpsprodpb/11BEF/production/_99778627_winters.jpg",
             "title": "Winter Olympics 2018: Doping ban, neutral Russians & Pyeongchang medal hopes",
             "summary": "What was the point of banning Russia from the Winter Olympics when 169 of their athletes are still being allowed to compete as neutrals? "}]


def pipeline_test(passed_url):
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
    similar_articles = find_similar_articles(article_keywords)
    similar_article_time = time.time()
    print("Similar articles:\n\t{:s}".format("\n\t".join([a["title"] for a in similar_articles])))
    print("Finding similar articles took " + str(similar_article_time - extraction_time) + " seconds")

    # get heuristics db
    if USE_CACHING:
        db = HeuristicsDB()
        # check for db entry for initial article
        # TODO: consider checking when we last ran heuristics
        article = db.read_article(passed_url)

    if USE_CACHING and article is None:
        # run heuristics on initial article
        initial_heuristics = classify({'text': article.cleaned_text})
        # write to DB
        db.write_article(passed_url, initial_heuristics)

        # logging info
        initial_heuristic_time = time.time()
        print("Running initial heuristics took " + str(initial_heuristic_time - similar_article_time) + " seconds")
    else:
        # use cached heuristics if possible
        initial_heuristics = article['heuristics']

        # logging info
        initial_heuristic_time = time.time()
        print("Got cached initial heuristics, took " + str(initial_heuristic_time - similar_article_time) + " seconds")

    # run heuristics on each similar article
    comparison_heuristics_list = []
    for entry in similar_articles:
        try:
            url = entry['url']

            if USE_CACHING:
                # check if we have cached this article
                # TODO: consider checking when we last ran heuristics
                cached_article = db.read_article(url)

                # TODO: consider caching this info
                comparison_article = extract_content(url)

            if USE_CACHING and cached_article is None:
                # run heuristics
                comparison_heuristics = classify({'text': comparison_article.cleaned_text})
                # write to db
                db.write_article(url, comparison_heuristics)
            else:
                # use heuristics from database
                comparison_heuristics = cached_article['heuristics']

            # add article to list for suitability calculation
            comparison_heuristics_list.append(({'article': comparison_article, 'url': url}, comparison_heuristics))
        except:
            print('error extracting:', url)

    comparison_heuristic_time = time.time()
    print("Running comparison heuristics took " + str(comparison_heuristic_time - initial_heuristic_time) + " seconds")

    # run suitability calculations
    suitable_articles = get_suitable_articles(initial_heuristics, comparison_heuristics_list)[:3]
    print("Suitable articles:\n\t{:s}".format("\n\t".join([a['title'] for a, _ in suitable_articles])))
    suitability_calculation_time = time.time()
    print("Running suitability calculations took " + str(
        suitability_calculation_time - comparison_heuristic_time) + " seconds")

    # format for sending to plugin
    articles_to_return = []
    for suitable_article, _ in suitable_articles:
        ret_article = {"link": suitable_article['url'],
                       "imageLink": "",
                       "title": suitable_article['title'],
                       "summary": '%s%s' % (suitable_article['text'][:100], '...')
                       }
        articles_to_return.append(ret_article)

    # return 3 suitable articles
    return articles_to_return
