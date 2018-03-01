from .backend_bing import BackendBing
from .backend_google import BackendGoogle
import itertools
from urllib.parse import urldefrag

backends = [BackendBing(), BackendGoogle()]


# based on https://stackoverflow.com/a/480227/1763627
def remove_duplicates(seq, comparison_mapper=lambda x: x):
    seen = set()
    return [x for x in seq if not (comparison_mapper(x) in seen or seen.add(comparison_mapper(x)))]


# de-duplicate on the url without query string
def remove_duplicates_on_url(articles):
    return remove_duplicates(articles, lambda x: urldefrag(x['url'])[0])


# https://stackoverflow.com/a/21482016/1763627
def interleave(*iters):
    """
    Given two or more iterables, return a list containing
    the elements of the input list interleaved.

    >>> interleave([1,2,3], ['a', 'b', 'c', 'd'])
    [1, 'a', 2, 'b', 3, 'c', 'd']
    """
    return [x for x in itertools.chain.from_iterable(itertools.zip_longest(*iters)) if x]


def find_similar_articles(keywords):
    """
    Format: [{'title':<title>, 'url':<url>}, ...]
    """
    backend_results = [b.get_similar_for_keywords(keywords) for b in backends]

    # Interleave & de-duplicate results
    results = remove_duplicates_on_url(interleave(*backend_results))
    return results


def get_similar_article_backend_results(keywords):
    return [
        dict(name=b.backend_name,
             shortname=b.__class__.__name__,
             results=b.get_similar_for_keywords(keywords)) for b in backends]
