from content_extraction.goose.extract_content import extract_content

urls = [
    "http://www.bbc.co.uk/news/uk-politics-42867668",
    "http://www.dailymail.co.uk/tvshowbiz/article-5328767/Kim-Kardashian-hits-cultural-appropriation.html",
    "https://www.theguardian.com/lifeandstyle/2012/sep/07/kim-kardashian-life-as-brand",
    "https://www.hellomagazine.com/tags/kim-kardashian/",
    "https://www.vanityfair.com/news/2017/12/donald-trump-wines",
    "https://www.nbcnews.com/politics/donald-trump/trump-s-gripes-against-mccabe-included-wife-s-politics-comey-n842161"
]

articles = [extract_content(url) for url in urls]

for article in articles:
    auth = article.authors
    text = article.cleaned_text
    #im = article.top_image
    title = article.title

    print("Title: ", title)
    print("Author: ", auth)
    print("Cleaned text: ", text)
    print("\n")