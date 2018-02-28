from content_extraction.goose.extract_content_goose import ExtractContentGoose
from content_extraction.newspaper.extract_content_newspaper import ExtractContentNewspaper


backends = [ExtractContentGoose(), ExtractContentNewspaper()]


def extract_content(url, enable_image_fetching=False, timeout=None, user_agent=None):
    # use all of the backends to get results
    extraction_results = [b.extract_content(url, enable_image_fetching=enable_image_fetching, timeout=timeout, user_agent=user_agent) for b in backends]
    # merge the results and return
    return merge_results(extraction_results)


def merge_results(results):
    # TODO: merge in a more meaningful way, get more backends integrated
    # TODO: don't make separate GET reqs
    basic = results[0]
    basic['keywords'] = list(set(basic['keywords']).union(results[1]['keywords']))
    basic['date'] = results[1]['date']
    return basic

