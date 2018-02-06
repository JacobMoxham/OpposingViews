import unittest

import classifiers


class TestClassifiers(unittest.TestCase):
    def test_left_wing(self):
        text = "The rightwing president tweeted about fake news last week"
        self.assertEqual(classifiers.classify({'text': text})['source_politics'], 0)

    def test_right_wing(self):
        text = "President Donald Trump will make America great by bombing migrant terorrists"
        self.assertEqual(classifiers.classify({'text': text})['source_politics'], 1)


if __name__ == '__main__':
    unittest.main()
