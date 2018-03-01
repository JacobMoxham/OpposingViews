import unittest
import itertools
from aws_python.similar_articles.backend import SimilarArticleBackend
from aws_python.similar_articles.backend_google import BackendGoogle
from aws_python.similar_articles.backend_bing import BackendBing
import aws_python.similar_articles.frontend as frontend


class TestBackends(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'backend'):
            raise unittest.SkipTest

    def test_has_name(self):
        self.assertTrue(self, len(self.backend.backend_name) > 0)

    def test_gives_results(self):
        # TODO: these tests really shouldn't go over-the-wire.
        # They really really need fixed data.
        # Fix when I have the time to do proper dependency injection.
        self.assertTrue(self, len(self.backend.get_similar_for_keywords(["Trump"])) > 0)


class TestBackendGoogle(TestBackends):
    def setUp(self):
        self.backend = BackendGoogle()
        super().setUp()


class TestBackendBing(TestBackends):
    def setUp(self):
        self.backend = BackendBing()
        super().setUp()


class TestFrontend(unittest.TestCase):
    def test_remove_duplicates(self):
        self.assertEqual(frontend.remove_duplicates([1, 2, 3]), [1, 2, 3])
        self.assertEqual(frontend.remove_duplicates([1, 1, 3, 2, 2, 1]), [1, 3, 2])
        self.assertEqual(frontend.remove_duplicates([]), [])
        self.assertEqual(frontend.remove_duplicates([1, 2], lambda x: 0), [1])

        counter = itertools.count(1)
        self.assertEqual(frontend.remove_duplicates([1, 1, 2, 2, 3, 3, 2, 1], lambda x: next(counter)), [1, 1, 2, 2, 3, 3, 2, 1])

    def test_remove_duplicate_urls(self):
        input_urls = [
            {'url': 'http://example.com/test.html'},
            {'url': 'http://example.com/test.html#t2'},
            {'url': 'http://example.com/test.html#t3'},
            {'url': 'http://example.com/test2.html'}
        ]

        target_urls = [
            {'url': 'http://example.com/test.html'},
            {'url': 'http://example.com/test2.html'}
        ]

        self.assertEqual(frontend.remove_duplicates_on_url(input_urls), target_urls)

if __name__ == '__main__':
    unittest.main()
