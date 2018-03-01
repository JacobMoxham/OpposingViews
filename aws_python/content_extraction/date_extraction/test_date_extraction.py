from extract_date import ExtractDate


urls = [
    "http://www.bbc.co.uk/news/uk-politics-42867668",
    "http://www.dailymail.co.uk/tvshowbiz/article-5328767/Kim-Kardashian-hits-cultural-appropriation.html",
    "https://www.theguardian.com/lifeandstyle/2012/sep/07/kim-kardashian-life-as-brand",
    "https://www.hellomagazine.com/tags/kim-kardashian/",
    "https://www.vanityfair.com/news/2017/12/donald-trump-wines",
    "https://www.nbcnews.com/politics/donald-trump/trump-s-gripes-against-mccabe-included-wife-s-politics-comey-n842161"
]

date = ExtractDate()




for url in urls:
    	
    
    print("Date: ", date.extract_date(url)['date'])
    
    
print("\n")
