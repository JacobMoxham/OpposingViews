import mongo.database_access as mongo

# Create test document
url = "test url"
heuristic = {'sentiment': 0.7, 'source_politics': 0.1, 'opinion_strength': 0.5, 'seriousness': 0.3}

# Get db instance
db = mongo.get_heuristics_database()

# Write the article to the database
mongo.write_article(db, url, heuristic)

# Read it back
article = mongo.read_article(db, url)

# Print article
print(article)
assert(article['url'] == url)
assert(article['heuristics'] == heuristic)

#Try reading a url we have no entry for
empty = mongo.read_article(db, "")
print("Is result for url with no article none? :", empty == None)
assert(empty == None)