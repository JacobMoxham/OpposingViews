from content_extraction.goose.extract_content_goose import ExtractContentGoose


backends = [ExtractContentGoose()]


def extract_content(url):
    # use all of the backends to get results
    extraction_results = [b.extract_content(url) for b in backends]
    # merge the results and return
    return merge_results(extraction_results)


def merge_results(results):
    # TODO: merge in a more meaningful way, get more backends integrated
    return results[0]