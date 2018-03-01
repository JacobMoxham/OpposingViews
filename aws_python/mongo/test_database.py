import mongo.database_access as mongo

# create test document
url = "test url"
url2 = 'http://www.bbc.co.uk/news/world-us-canada-43066226'
heuristics = {'sentiment': 0.7, 'source_politics': 0.1, 'opinion_strength': 0.5, 'seriousness': 0.3}
heuristics2 = {'source_politics': 0}

# get db instance
db = mongo.HeuristicsDB()

# write the article to the database
db.write_article(url, heuristics)
db.write_article(url2, heuristics2)

# read it back
article = db.read_article(url)
article2 = db.read_article(url2)

# print article
print(article)
assert(article['url'] == url)
assert(article['heuristics'] == heuristics)

# try reading a url we have no entry for
empty = db.read_article("")
print("Is result for url with no article none? :", empty is None)
assert(empty is None)