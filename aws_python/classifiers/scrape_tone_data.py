#!/usr/bin/env python3

import sys
import os

import requests
from classifiers.tone_classifier_training import getFolderRoot
from bs4 import BeautifulSoup
from content_extraction.extract_content import extract_content
from urllib.parse import urljoin
import re

test = False
def getSeed(doctype):
    return max([0] + [int(x) + 1 for x in os.listdir(getFolderRoot(doctype)) if x.isdigit()])

seed = {x : getSeed(x) for x in ['neutral', 'opinion']}

def getGeneric(
        num_documents,
        doctype,
        url_base,
        url_selection = lambda x : x,
        url_wrangling = lambda x : x,
        ):
    global seed
    linklistname = getFolderRoot(doctype) + 'links'

    r = requests.get(url_base)
    soup = BeautifulSoup(r.content, 'lxml')
    i = 0
    try:
        with open(linklistname) as f:
            seen_links = [line.rstrip() for line in f if line != '\n']
    except FileNotFoundError:
        seen_links = []

    for link in soup.find_all('a'):
        url = str(url_wrangling(link.get('href')))
        if url_selection(url) and i < num_documents and url not in seen_links:
            seen_links.append(url)
            if test:
                print(url)
            else:
                with open(getFolderRoot(doctype) + str(seed[doctype]), 'w') as f:
                    content = extract_content(url)
                    f.write(content['title'] + '\n\n' + content['text'])
            seed[doctype] = seed[doctype] + 1
            i = i + 1
        elif i == num_documents:
            break
        
    if not test:
        with open(linklistname, 'w') as f:
            for link in seen_links:
                f.write("%s\n" % link)
    

def getBBCNews(num_documents = 20):
    base_site = 'http://www.bbc.co.uk/news'
    return getGeneric(num_documents,
        'neutral',
        base_site,
        lambda url : re.search("\d{8}$", url) and (not re.search('live', url)),
        lambda url : urljoin(base_site, url)
    )

def containsDate(url):
    return re.search('\d{4}/\d{2}/\d{2}', url)

def getFoxNews(num_documents = 20):
    base_site = 'http://www.foxnews.com'
    getGeneric(num_documents, 'neutral',
            base_site,
            lambda url :  (not re.search('video|opinion|insider\.fox', url)) and containsDate(url),
            lambda url : re.sub("^//", "http://", url)
            )

def getFoxOpinions(num_documents = 20):
    base_site = "http://www.foxnews.com/opinion.html"
    getGeneric(num_documents, 'opinion',
            base_site,
            lambda url : containsDate(url),
            lambda url : urljoin(base_site, url)
            )

def getNYTimesNews(num_documents = 20):
    getGeneric(
            num_documents,
            'neutral',
            'https://www.nytimes.com/',
            lambda url : containsDate(url) and not re.search('/well/|interactive|#comments|opinion', url)
            )

def getNYTimesOpinions(num_documents = 20):
    getGeneric(
            num_documents,
            'opinion',
            'https://www.nytimes.com/section/opinion',
            lambda url : containsDate(url)
            )

def getNYPostNews(num_documents = 20):
    getGeneric(
            num_documents,
            'neutral',
            'https://nypost.com/',
            lambda url : containsDate(url) and "pagesix.com" not in url,
            )

def getNYPostOpinions(num_documents = 20):
    getGeneric (
            num_documents,
            'opinion',
            'https://nypost.com/opinion/',
            lambda url : containsDate(url),
            )

def getWashingtonPostOpinions(num_documents = 20):
    getGeneric(
            num_documents,
            'opinion',
            'https://www.washingtonpost.com/opinions',
            lambda url : containsDate(str(url)) and '/opinions/' in url,
            )

def getReutersNews(num_documents = 20):
    base_site =  'https://uk.reuters.com/'
    getGeneric(
            num_documents,
            'neutral',
            base_site,
            lambda url : '/article/' in url,
            lambda url : urljoin(base_site, url),
            )

def getAlJazeeraNews(num_documents = 20):
    base_site = 'https://www.aljazeera.com/'
    getGeneric(
            num_documents,
            'neutral',
            base_site,
            lambda url : re.search('/\d{4}/\d{2}/', str(url)) and '/news/' in str(url),
            lambda url : urljoin(base_site, url),
        )

def getBloombergOpinions(num_documents = 20):
    base_site = 'https://www.bloomberg.com/view/'
    getGeneric(
            num_documents,
            'opinion',
            base_site,
            lambda url : url is not None and re.search("^https://www\.bloomberg\.com", url) and re.search('\d{4}-\d{2}-\d{2}', url),
            )

def getAtlanticOpinions(num_documents = 20):
    base_site = 'https://www.theatlantic.com/world/'
    getGeneric(
            num_documents,
            'opinion',
            base_site,
            lambda url : re.search("/archive/\d{4}/\d{2}/", str(url)),
            )

def getTimesOfIndiaNews(num_documents = 20):
    base_site = 'https://timesofindia.indiatimes.com/'
    getGeneric(
            num_documents,
            'neutral',
            base_site,
            lambda url : '/news/' in url
            )
def getEconomistOpinion(num_documents = 20):
    base_site = 'https://www.economist.com/latest-updates'
    getGeneric(num_documents,
            'opinion',
            base_site,
            lambda url : '/blogs/' in url and re.search('\d{4}/\d{2}', url),
            lambda url : urljoin(base_site, url)
            ) 

def getEconomistNews(num_documents = 20):
    base_site = 'https://www.economist.com/latest-updates'
    getGeneric(num_documents,
            'neutral',
            base_site,
            lambda url : '/news/' in url,
            lambda url : urljoin(base_site, url)
            ) 

def getUSATodayNews(num_documents = 20):
    base_site = 'https://www.usatoday.com/news/'
    getGeneric(num_documents,
            'neutral',
            base_site,
            lambda url : '/story/news/' in url,
            lambda url : urljoin(base_site, url)
            )

if __name__ == '__main__':
    getBBCNews()
    getFoxNews()
    getNYTimesNews()
    getNYPostNews()
    getWashingtonPostOpinions()
    getReutersNews()
    getAlJazeeraNews()
    getFoxOpinions()
    getNYTimesOpinions()
    getBloombergOpinions()
    getNYPostOpinions()
    getAtlanticOpinions()
    getEconomistOpinion()
    getEconomistNews()
    getUSATodayNews()
