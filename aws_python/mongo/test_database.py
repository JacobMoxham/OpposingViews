import mongo.database_access as mongo

# create test document
url = "test url"
heuristic = {'sentiment': 0.7, 'source_politics': 0.1, 'opinion_strength': 0.5, 'seriousness': 0.3}

# get db instance
db = mongo.HeuristicsDB()

# write the article to the database
db.write_article(url, heuristic)

# read it back
article = db.read_article(url)

# print article
print(article)
assert(article['url'] == url)
assert(article['heuristics'] == heuristic)

# try reading a url we have no entry for
empty = db.read_article("")
print("Is result for url with no article none? :", empty is None)
assert(empty is None)