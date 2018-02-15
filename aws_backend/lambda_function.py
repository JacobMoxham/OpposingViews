from bs4 import BeautifulSoup
import urllib

def lambda_handler(event, context):
    src = event['src']
    soup = BeautifulSoup(urllib.parse.unquote(src), 'html.parser')
    return [{"link": "http://www.bbc.co.uk/news/uk-politics-42929071", "imageLink": "https://ichef.bbci.co.uk/news/320/cpsprodpb/AFA4/production/_99746944_gettyimages-531840456.jpg", "title": "Jacob Rees-Mogg says Treasury 'fiddling figures' on Brexit", "summary": "Prominent Brexiteer Jacob Rees-Mogg has said he believes Treasury officials are 'fiddling the figures' on Brexit."}, {"link": "http://www.bbc.co.uk/sport/winter-olympics/42840632", "imageLink": "https://ichef.bbci.co.uk/onesport/cps/480/cpsprodpb/11BEF/production/_99778627_winters.jpg", "title": "Winter Olympics 2018: Doping ban, neutral Russians & Pyeongchang medal hopes", "summary": "What was the point of banning Russia from the Winter Olympics when 169 of their athletes are still being allowed to compete as neutrals? "}]
