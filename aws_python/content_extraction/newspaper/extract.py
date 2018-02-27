from newspaper import Article
import urllib.request,json
from xml.dom import minidom
from bs4 import BeautifulSoup

url = "http://www.bbc.co.uk/news/uk-england-london-43058159"
response = urllib.request.urlopen(url)
html = response.read().decode()


#soup for theguardian
soup = BeautifulSoup(html, "html.parser")
#published_date = soup.find (property="article:published_time")
#print (published_date['content'])

#for meta in soup.find_all('meta'):
#    if meta.get('name') == 'author': print(meta.get('content')) #also the keywords
     
#soup for bbc

details_json = json.loads(soup.find (type = "application/ld+json").string) # useful info about the article
published_date = details_json['datePublished']
print (json.dumps(details_json,sort_keys=True,indent=4, separators=(',', ': ')))
print (published_date)


#Newspaper
article = Article (url)
article.download()
article.parse()
print (article.authors)
print (article.publish_date)
print (article.title)


