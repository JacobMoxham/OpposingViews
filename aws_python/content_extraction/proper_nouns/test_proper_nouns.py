from content_extraction.newspaper.extract_content_newspaper import ExtractContentNewspaper
from content_extraction.proper_nouns.extract_proper_nouns import ExtractProperNouns

urls = [
    "http://www.bbc.co.uk/news/uk-politics-42867668",
    "http://www.dailymail.co.uk/tvshowbiz/article-5328767/Kim-Kardashian-hits-cultural-appropriation.html",
    "https://www.theguardian.com/lifeandstyle/2012/sep/07/kim-kardashian-life-as-brand",
    "https://www.hellomagazine.com/tags/kim-kardashian/",
    "https://www.vanityfair.com/news/2017/12/donald-trump-wines",
    "https://www.nbcnews.com/politics/donald-trump/trump-s-gripes-against-mccabe-included-wife-s-politics-comey-n842161"
]

n = ExtractContentNewspaper()
pn = ExtractProperNouns()

articles = [n.extract_content(url) for url in urls]

for article in articles:
    	
    print (article['title'])
    print("Title: ", pn.extract_proper_nouns(article['title']))

    
print("\n")
