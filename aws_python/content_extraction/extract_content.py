from content_extraction.goose.extract_content_goose import ExtractContentGoose
from content_extraction.newspaper.extract_content_newspaper import ExtractContentNewspaper
from keyword_extraction.extract_keywords import keywords


extraction_backends = [ExtractContentGoose().extract_content,
                       ExtractContentNewspaper().extract_content
                       ]


def extract_content(url, enable_image_fetching=False, timeout=None, user_agent=None, extraction_method=0,
                    keyword_method=0, keyword_amount=5):

    extraction_results = extraction_backends[extraction_method](url, enable_image_fetching=enable_image_fetching,
                                                                timeout=timeout, user_agent=user_agent)

    extraction_results['keywords'] = keywords(extraction_results['title'], extraction_results['text'],
                                              ipl=keyword_method, n=keyword_amount)

    return extraction_results
