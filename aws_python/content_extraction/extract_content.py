from content_extraction.goose.extract_content_goose import ExtractContentGoose
from content_extraction.newspaper.extract_content_newspaper import ExtractContentNewspaper
from content_extraction.proper_nouns.extract_proper_nouns import ExtractProperNouns
from keyword_extraction.extract_keywords import keywords


extraction_backends = [ExtractContentGoose(), ExtractContentNewspaper()]
keywords_backends = [ExtractProperNouns()]


def extract_content(url, enable_image_fetching=False, timeout=None, user_agent=None, method=2):
    # TODO: choose method
    # TODO: clean up this messy code

    if method == 1:
        # use all of the backends to get results
        extraction_results = \
            [b.extract_content(url, enable_image_fetching=enable_image_fetching, timeout=timeout, user_agent=user_agent)
             for b in extraction_backends]
        # merge the results and return
        return merge_results(extraction_results)
    if method == 2:
        extraction_results = \
            extraction_backends[0].extract_content(url, enable_image_fetching=enable_image_fetching,
                                                   timeout=timeout, user_agent=user_agent)
        extraction_results['keywords'] = keywords(extraction_results['title'], extraction_results['text'])
        return extraction_results
    if method == 3:
        extraction_results = \
            extraction_backends[0].extract_content(url, enable_image_fetching=enable_image_fetching,
                                                   timeout=timeout, user_agent=user_agent)
        extraction_results['keywords'] = keywords(extraction_results['title'], extraction_results['text'])
        extraction_results['keywords'] = list(set(extraction_results['keywords']).union(
            keywords_backends[0].extract_proper_nouns(extraction_results['text'])))
        return extraction_results


def merge_results(results):
    # TODO: merge in a more meaningful way, get more backends integrated
    # TODO: don't make separate GET reqs
    basic = results[0]
    basic['keywords'] = list(set(basic['keywords']).union(results[1]['keywords']))
    basic['date'] = results[1]['date']
    return basic

