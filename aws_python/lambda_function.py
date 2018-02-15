from content_extraction.goose.extract_content import extract_content
from similar_articles.frontend import find_similar_articles
from classifiers.classifiers import classify
from suitability_scoring.calculate_suitability import get_suitable_articles

from bs4 import BeautifulSoup
import urllib

def lambda_handler(event, context):
    url = event['link']
    return pipeline_test(url)


def test(event):
    soup = BeautifulSoup(urllib.parse.unquote(src), 'html.parser')
    return [{"link": "http://www.bbc.co.uk/news/uk-politics-42929071",
             "imageLink": "https://ichef.bbci.co.uk/news/320/cpsprodpb/AFA4/production/_99746944_gettyimages-531840456.jpg",
             "title": "Jacob Rees-Mogg says Treasury 'fiddling figures' on Brexit",
             "summary": "Prominent Brexiteer Jacob Rees-Mogg has said he believes Treasury officials are 'fiddling the figures' on Brexit."},
            {"link": "http://www.bbc.co.uk/sport/winter-olympics/42840632",
             "imageLink": "https://ichef.bbci.co.uk/onesport/cps/480/cpsprodpb/11BEF/production/_99778627_winters.jpg",
             "title": "Winter Olympics 2018: Doping ban, neutral Russians & Pyeongchang medal hopes",
             "summary": "What was the point of banning Russia from the Winter Olympics when 169 of their athletes are still being allowed to compete as neutrals? "}]

def pipeline_test(passed_url):
    article = extract_content(passed_url)
    similar_articles = find_similar_articles(article.meta_keywords)
    initial_heuristics = classify({'text': article.cleaned_text})

    comparison_heuristics_list = []
    for entry in similar_articles:
        try:
            url = entry['url']
            comparison_article = extract_content(url)
            comparison_heuristics = classify({'text': comparison_article.cleaned_text})
            comparison_heuristics_list.append(({'article': article, 'url': url}, comparison_heuristics))
        except:
            print(url)

    suitable_articles = get_suitable_articles(initial_heuristics, comparison_heuristics_list)[:3]
    articles_to_return = []
    for article, _ in suitable_articles:
        ret_article = {"link": article['url'],
                       "imageLink": "",
                       "title": article['article'].title,
                       "summary": article['article'].cleaned_text[:100]}
        articles_to_return.append(ret_article)

    return articles_to_return
