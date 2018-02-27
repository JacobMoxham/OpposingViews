from keyword_extraction.extract_keywords import keywords
from content_extraction.extract_content import extract_content
from keyword_extraction.tfidf import get_idf

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'

urls = ["http://www.bbc.co.uk/news/uk-politics-42867668",
        "http://www.dailymail.co.uk/tvshowbiz/article-5328767/Kim-Kardashian-hits-cultural-appropriation.html",
        #"https://www.theguardian.com/lifeandstyle/2012/sep/07/kim-kardashian-life-as-brand",
        "https://www.hellomagazine.com/tags/kim-kardashian/",
        "https://www.vanityfair.com/news/2017/12/donald-trump-wines",
        "https://www.nbcnews.com/politics/donald-trump/trump-s-gripes-against-mccabe-included-wife-s-politics-comey-n842161",
        'http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2',
        'http://chrisgreybrexitblog.blogspot.co.uk/2018/02/britains-brexit-self-punishment.html',
        'https://www.oneangrygamer.net/2018/01/vice-media-anti-gamergate-outlet-fires-mike-germano-sexual-misconduct/50379/',
        # 'https://www.theguardian.com/technology/2017/sep/24/zoe-quinn-gamergate-online-abuse',
        'http://www.theweek.co.uk/90229/what-is-the-capital-of-israel',
        'https://www.washingtonpost.com/world/israel-blasts-iran-deal-as-dark-day-in-history/2015/07/14/feba23ae-0018-403f-82f3-3cd54e87a23b_story.html?utm_term=.2f548f59e6cb',
        'https://dailystormer.name/goycott-business-works-with-communists-to-fire-tony-hovater-but-now-were-fighting-back/',
        'https://www.snopes.com/four-times-more-stabbed-than-rifles-any-kind/',
        # 'https://www.theguardian.com/commentisfree/2015/jan/06/real-american-sniper-hate-filled-killer-why-patriots-calling-hero-chris-kyle',
        'https://www.theguardian.com/commentisfree/2015/oct/30/indonesia-fires-disaster-21st-century-world-media',
        ]

# idf, iwi = get_idf()

for url in urls:
    article = extract_content(url, user_agent=USER_AGENT)

    print(article['title'])
    print('Simple')
    print(keywords(article['title'], article['text'], n=5, ipl=2))
    print('Weighted')
    print(keywords(article['title'], article['text'], n=5, ipl=3))
    print('Rlms Method')
    print(keywords(article['title'], article['text'], n=5, ipl=1))
    # print('+Metadata')
    # print(keywords(article['title'], article['text'], n=5))
    print()
