import unittest
from aws_python.similar_articles.backend import SimilarArticleBackend
from aws_python.similar_articles.backend_google import BackendGoogle
from aws_python.similar_articles.backend_bing import BackendBing


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
        self.backend: SimilarArticleBackend = BackendGoogle()
        super().setUp()


class TestBackendBing(TestBackends):
    def setUp(self):
        self.backend: SimilarArticleBackend = BackendBing()
        super().setUp()


if __name__ == '__main__':
    unittest.main()
