import json
import concurrent.futures

from content_extraction.extract_content import extract_content

OUTPUT_FILE = 'left_articles.json'
REREQUEST_STORED = True
TIMEOUT = 20
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'

with open('classifiers/reddit_scraper/left_urls.json') as f:
    subreddits = json.load(f)

with open(OUTPUT_FILE) as f:
    contents = json.load(f)


def get_url(url):
    return extract_content(url, enable_image_fetching=False, timeout=TIMEOUT, user_agent=USER_AGENT)


for sr in subreddits:
    print(sr)
    if not REREQUEST_STORED and sr in contents:
        print('Skipped')
        continue
    contents[sr] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(get_url, url): url for url in subreddits[sr]}
        length = len(futures)
        for index, future in enumerate(concurrent.futures.as_completed(futures)):
            try:
                data = future.result()
                print(100*index / length)
                contents[sr][futures[future]] = data
            except Exception as e:
                print(e, futures[future])

    with open('left_articles.json', 'w') as f:
        json.dump(contents, f)
