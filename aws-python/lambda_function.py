from bs4 import BeautifulSoup
import urllib
import json

def lambda_handler(event, context):
    src = event['src']
    soup = BeautifulSoup(urllib.parse.unquote(src), 'html.parser')
    return {'title': soup.title.string}
