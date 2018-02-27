import re
import json

from praw import Reddit

from reddit_creds import CLIENT_ID, CLIENT_SECRET, PASSWORD, USER_AGENT, USERNAME

r = Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, password=PASSWORD, user_agent=USER_AGENT, username=USERNAME)

URL_BLACKLIST = ['.*reddit\.com.*',
                 '.*sli\.mg.*',
                 '.*redd\.it.*',
                 '.*imgur\.com.*',
                 '.*liveleak\.com.*',
                 '.*reddituploads\.com.*',
                 '.*twitter\.com.*',
                 '.*twimg\.com.*',
                 '.*youtube\.com.*',
                 '.*youtu\.be.*',
                 '.*\.png',
                 '.*\.jpg',
                 '.*\.jpeg',
                 '.*\.gif',
                 '.*\.mp3',
                 '.*\.mp4',
                 ]

left_subreddits = ['Anarchism', 'socialism', 'progressive', 'democrats', 'Liberal', 'demsocialist', 'GreenParty', 'Marxism', 'feminisms', 'SocialDemocracy', 'chomsky', 'occupywallstreet',]

right_subreddits = ['The_Donald', 'Conservative', 'new_right', 'Republican', 'republicans', 'conservatives',]

result = {}

for sr in left_subreddits:
    print(sr)
    result[sr] = []
    for submission in r.subreddit(sr).top('all', limit=10000):
        if any(re.match(p, submission.url) for p in URL_BLACKLIST):
            continue

        result[sr].append(submission.url)

with open('left_urls.json', 'w') as f:
    json.dump(result, f)

for sr in right_subreddits:
    print(sr)
    result[sr] = []
    for submission in r.subreddit(sr).top('all', limit=10000):
        if any(re.match(p, submission.url) for p in URL_BLACKLIST):
            continue

        result[sr].append(submission.url)

with open('right_urls.json', 'w') as f:
    json.dump(result, f)
