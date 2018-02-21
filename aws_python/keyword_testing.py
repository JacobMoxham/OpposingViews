from keyword_extraction.extract_keywords import keywords
from content_extraction.extract_content import extract_content

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'

urls = ["http://www.bbc.co.uk/news/uk-politics-42867668",
        "http://www.dailymail.co.uk/tvshowbiz/article-5328767/Kim-Kardashian-hits-cultural-appropriation.html",
        "https://www.theguardian.com/lifeandstyle/2012/sep/07/kim-kardashian-life-as-brand",
        "https://www.hellomagazine.com/tags/kim-kardashian/",
        "https://www.vanityfair.com/news/2017/12/donald-trump-wines",
        "https://www.nbcnews.com/politics/donald-trump/trump-s-gripes-against-mccabe-included-wife-s-politics-comey-n842161",
        ]

for url in urls:
    article = extract_content(url, user_agent=USER_AGENT)
    print(article['title'])
    print('New')
    print(keywords(article['title'], article['text'], n=8))
    print('Old')
    print(article['keywords'])
    print()
