from .backend_bing import BackendBing
from .backend_google import BackendGoogle
import itertools

backends = [BackendBing(), BackendGoogle()]


# https://stackoverflow.com/a/480227/1763627
def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


# https://stackoverflow.com/a/21482016/1763627
def interleave(*iters):
    """
    Given two or more iterables, return a list containing
    the elements of the input list interleaved.

    >>> interleave(*[x, y])
    [1, 9, 2, 8, 3, 7, 4, 6, 5]
    """
    return [x for x in itertools.chain.from_iterable(itertools.zip_longest(*iters)) if x]


def find_similar_articles(keywords):
    """
    Format: [{'title':<title>, 'url':<url>}, ...]
    """
    backend_results = [b.get_similar_for_keywords(keywords) for b in backends]
    # TODO: remove duplicates
    # can't use the remove_duplicates function as dicts don't behave well in sets
    results = interleave(*backend_results)
    return results


def get_similar_article_backend_results(keywords):
    return [
        dict(name=b.backend_name,
             shortname=b.__class__.__name__,
             results=b.get_similar_for_keywords(keywords)) for b in backends]
