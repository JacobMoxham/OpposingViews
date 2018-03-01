import unittest
from aws_python.dedupe_articles.hash_functions import hash_dirty_text, compare_similarities
from aws_python.dedupe_articles.deduplicate_articles import get_unique_hashes


class TestHashingDirtyText(unittest.TestCase):
    def test_hashes_ok(self):
        self.assertEqual(hash_dirty_text("Hello, World!\nthis is a test."), hash_dirty_text("helloworldthisisatest"))
        self.assertEqual(hash_dirty_text("helloworld"), "3:iKJP:b") # obviously this will break if we change algo

    def test_similarity_scoring(self):
        self.assertGreaterEqual(compare_similarities(hash_dirty_text("hello world"), hash_dirty_text("hello world")), 0.5)
        self.assertGreaterEqual(compare_similarities(hash_dirty_text("hello world"), hash_dirty_text("HELLO WORLD!!")), 0.5)
        self.assertLessEqual(compare_similarities(hash_dirty_text("hello world"), hash_dirty_text("oops what have I done my algo broke")), 0)


class TestRemovingDuplicates(unittest.TestCase):
    def test_removing_dupe_hashes(self):
        texts = [
            "original",
            "this is a short article but long enough to trigger the SSDeep thingy hopefully",
            "hello world",
            "Othis is a short article but long enough to trigger the SSDeep thingy hopefully",
            "this too is unique",
            "original"
        ]
        hashes = [hash_dirty_text(t) for t in texts]
        print(hashes)
        deduped = get_unique_hashes(hashes[1:], [hashes[0]])
        self.assertEqual(deduped, [1, 1, 0, 1, 0])


if __name__ == '__main__':
    unittest.main()
