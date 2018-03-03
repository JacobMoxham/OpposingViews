from keyword_extraction.extract_keywords import keywords
from content_extraction.extract_content import extract_content
from keyword_extraction.tfidf import get_idf

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'

urls = ["https://uk.reuters.com/article/uk-germany-cyber-russia/germany-says-its-government-computers-secure-after-isolated-hack-idUKKCN1GC2HN",
        "http://www.bbc.co.uk/news/uk-politics-42867668",
        "http://www.dailymail.co.uk/tvshowbiz/article-5328767/Kim-Kardashian-hits-cultural-appropriation.html",
        "https://www.hellomagazine.com/tags/kim-kardashian/",
        "https://www.vanityfair.com/news/2017/12/donald-trump-wines",
        "https://www.nbcnews.com/politics/donald-trump/trump-s-gripes-against-mccabe-included-wife-s-politics-comey-n842161",
        'http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2',
        'http://chrisgreybrexitblog.blogspot.co.uk/2018/02/britains-brexit-self-punishment.html',
        'https://www.oneangrygamer.net/2018/01/vice-media-anti-gamergate-outlet-fires-mike-germano-sexual-misconduct/50379/',
        'http://www.theweek.co.uk/90229/what-is-the-capital-of-israel',
        'https://www.washingtonpost.com/world/israel-blasts-iran-deal-as-dark-day-in-history/2015/07/14/feba23ae-0018-403f-82f3-3cd54e87a23b_story.html?utm_term=.2f548f59e6cb',
        'https://dailystormer.name/goycott-business-works-with-communists-to-fire-tony-hovater-but-now-were-fighting-back/',
        'https://www.snopes.com/four-times-more-stabbed-than-rifles-any-kind/',
        'https://www.theguardian.com/commentisfree/2015/oct/30/indonesia-fires-disaster-21st-century-world-media',
        'http://www.bbc.co.uk/news/uk-wales-north-east-wales-43153466',
        'http://www.foxnews.com/politics/2018/02/22/trump-calls-for-arming-teachers-raising-gun-purchase-age-to-stop-savage-sicko-shooters.html',
        'https://www.nytimes.com/2018/02/21/world/africa/nigeria-kidnapping-boko-haram-dapchi.html',
        'https://nypost.com/2018/02/21/anthony-swarzak-on-finding-his-slider-and-being-a-foodie-in-nyc/',
        'https://uk.reuters.com/article/uk-brazil-space/brazils-defence-minister-says-spacex-boeing-interested-in-launching-from-amazon-base-idUKKCN1G62BO?il=0',
        'https://www.aljazeera.com/news/2018/02/yemens-health-crisis-suspected-cases-bird-flu-180218090434368.html',
        'http://www.bbc.co.uk/news/stories-43158849',
        'http://www.foxnews.com/world/2018/02/21/turkish-offensive-in-kurdish-held-syrian-enclave-sets-up-collision-course-with-us.html',
        'https://www.nytimes.com/2018/02/23/world/asia/ivanka-trump-south-korea.html',
        'https://nypost.com/2018/02/22/sheriffs-officer-who-did-nothing-to-stop-florida-shooter-resigns/',
        'https://uk.reuters.com/article/uk-china-anbang-regulation/china-seizes-control-of-anbang-insurance-as-chairman-prosecuted-idUKKCN1G707C?il=0',
        'https://www.aljazeera.com/news/2016/05/syria-civil-war-explained-160505084119966.html',
        'http://www.bbc.co.uk/news/in-pictures-43031764',
        'http://www.foxnews.com/us/2018/02/26/marjory-stoneman-douglas-ice-hockey-team-wins-state-championship.html',
        'https://www.nytimes.com/2018/02/23/movies/black-panther-afrofuturism-costumes-ruth-carter.html',
        'https://nypost.com/2018/02/25/transgender-boy-wins-girls-state-wrestling-title-for-second-time/',
        'https://uk.reuters.com/article/uk-mideast-crisis-syria-coalition/syrian-observatory-u-s-led-coalition-strike-kills-25-idUKKCN1GA0TJ?il=0',
        'https://www.aljazeera.com/news/2018/02/deadly-suicide-car-bombings-hit-yemen-aden-180224160013787.html',
        'https://www.economist.com/news/business-and-finance/21737343-chinas-government-takes-control-its-would-be-financial-colossus-rapid-rise',
        'https://www.economist.com/news/middle-east-and-africa/21737335-former-aide-may-spill-beans-prime-minister-pressure-binyamin',
        'http://www.foxnews.com/politics/2018/02/27/ice-arrests-more-than-150-people-in-bay-area-following-democratic-mayors-warning.html',
        'http://www.foxnews.com/politics/2018/02/27/democrat-governors-pay-raises-to-cabinet-members-draw-scrutiny.html',
        'https://www.nytimes.com/2018/02/27/nyregion/percoco-albany-corruption-trial.html',
        'https://nypost.com/2018/02/28/ice-arrests-more-than-150-people-after-mayor-warned-of-impending-raid/',
        'https://nypost.com/2018/02/27/the-std-that-keeps-most-contestants-from-competing-on-the-bachelor/',
        'https://uk.reuters.com/article/uk-britain-eu-nireland/johnson-says-northern-irish-border-issue-being-used-to-frustrate-brexit-idUKKCN1GC0VP',
        'https://uk.reuters.com/article/uk-melrose-inds-m-a-gkn/proxy-shareholding-group-pirc-opposes-melrose-bid-for-gkn-idUKKCN1GC115?il=0',
        'https://www.aljazeera.com/news/2018/02/yemen-forces-multiply-fight-growing-al-qaeda-influence-180226145605190.html',
        'https://www.economist.com/news/business-and-finance/21737446-almost-decade-after-ponzi-scheme-collapsed-trustees-are-still-returning',
        'https://www.usatoday.com/story/news/politics/2017/08/21/secret-service-cant-pay-agents-because-trumps-frequent-travel-large-family/529075001/',
        'https://www.washingtonpost.com/news/opinions/wp/2018/02/22/personal-ownership-of-nuclear-weapons-may-be-legal-under-the-second-amendment/',
        'https://www.washingtonpost.com/news/opinions/wp/2018/02/22/yes-senator-rubio-you-are-bought-and-paid-for/',
        'http://www.foxnews.com/opinion/2018/02/21/america-has-two-gun-cultures-dont-blame-law-abiding-gun-owners-for-murders.html',
        'http://www.foxnews.com/opinion/2018/02/22/florida-shooting-shows-need-for-more-mental-health-programs.html',
        'https://www.nytimes.com/2018/02/22/opinion/campus-sexual-assault-punitive-justive.html',
        'https://www.nytimes.com/2018/02/21/opinion/white-rose-hitler-protest.html',
        'https://www.nytimes.com/2018/02/22/opinion/parkland-shooting-army-training.html',
        'https://www.nytimes.com/2018/02/21/opinion/boys-violence-shootings-guns.html',
        'https://www.nytimes.com/2018/02/22/opinion/free-speech-discomfort.html',
        'https://www.bloomberg.com/gadfly/articles/2018-02-22/mixing-a-pc-and-a-smartphone-is-a-great-idea-in-theory',
        'https://nypost.com/2018/02/21/sorry-trumps-campaign-wasnt-competent-enough-to-pull-off-collusion/',
        'https://nypost.com/2018/02/21/fake-photo-tells-the-truth-about-nys-pathetic-economic-development-schemes/',
        'https://nypost.com/2018/02/21/billy-graham-truly-was-americas-pastor/',
        'https://nypost.com/2018/02/22/why-george-washingtons-rules-matter-more-than-ever-today/',
        'https://nypost.com/2018/02/21/the-critics-are-wrong-the-obamas-presidential-portraits-are-a-huge-success/',
        'https://nypost.com/2018/02/21/percocos-pathetic-stereotyping-ploy/',
        'http://www.foxnews.com/opinion/2018/02/22/on-black-history-month-african-american-civil-rights-pioneer-reflects-on-todays-political-landscape.html',
        'http://www.foxnews.com/opinion/2018/02/20/sean-hannity-president-obama-was-warned-about-russian-meddling-and-did-nothing.html',
        'https://www.nytimes.com/2018/02/23/opinion/german-left-merkel-demorats.html',
        'https://www.nytimes.com/2018/02/21/opinion/fbi-eastern-europe.html',
        'https://www.nytimes.com/2018/02/21/opinion/populism-new-deal.html',
        'https://www.bloomberg.com/view/articles/2018-02-22/trump-infrastructure-plan-is-self-destructing',
        'https://nypost.com/2018/02/22/automatic-weapons-dont-belong-in-the-hands-of-everyone/',
        'https://nypost.com/2018/02/22/gun-control-activists-need-to-learn-a-little-sympathy/',
        'https://nypost.com/2018/02/22/yet-another-way-obamas-spies-apparently-exploited-the-trump-dossier/',
        'https://nypost.com/2018/02/22/deputy-who-didnt-stop-florida-shooting-thinks-he-did-a-good-job/',
        'https://pagesix.com/2018/02/22/whoopi-goldberg-clashes-with-monique-on-the-view/',
        ]

# idf, iwi = get_idf()

for url in urls:
    article = extract_content(url, user_agent=USER_AGENT)

    print(article['title'])
    print('Simple')
    print(keywords(article['title'], article['text'], n=5, ipl=3))
    print('Weighted')
    print(keywords(article['title'], article['text'], n=5, ipl=4))
    print('Rlms Method')
    print(keywords(article['title'], article['text'], n=5, ipl=2))
    print('Union+UNF Method')
    print(keywords(article['title'], article['text'], n=5, ipl=1))
    print()
