import unittest

from . import classifiers


class TestClassifiers(unittest.TestCase):
    def test_left_wing(self):
        text = "The rightwing president tweeted about fake news last week"
        self.assertEqual(classifiers.classify({'text': text})['source_politics'], 0)

    def test_right_wing(self):
        text = "President Donald Trump will make America great by bombing migrant terorrists"
        self.assertEqual(classifiers.classify({'text': text})['source_politics'], 1)

    def test_news(self):
        text =  'Heavy snowfall is hitting parts of the UK, causing road and rail disruption.'
        self.assertTrue(classifiers.classify({'text' : text})['source_tone'] > 0.5)

    def test_opinion(self):
        text = 'The sense that a Conservative government might be callous is not an unfamiliar one: the contention that actual deaths have resulted from discernible policies is one that only slick-looking men on magazine-format current affairs programmes put any gusto into denying. Yet there is a creeping suspicion that the government has completely ground to a halt. Crises don’t erupt, because there is nobody to deal with them. New policies can’t be announced, because there is nobody to make them. The regular business of the state, to maintain its institutions, react to challenge, find solutions, learn from mistakes and – at its very simplest – make sure its citizens survive, has been suspended. Brexit has been consuming all its oxygen since the referendum was announced. It is astonishing that such an amorphous, deadlocked project could have so much impact: but it has suffocated the government’s ability to respond to anything else.'
        self.assertTrue(classifiers.classify({'text' : text})['source_tone'] < 0.5)

    def test_positive_tone(self):
        text = 'This thing is awesome and amazing'
        classification = classifiers.classify({'text': text})
#        self.assertTrue(classification['source_positivity'] > 0.5)
        self.assertTrue(classification['source_sentiment'] > 0.5)

    def test_negative_tone(self):
        text = 'This thing is horrible and pointless'
        classification = classifiers.classify({'text' : text})
#        self.assertTrue(classification['source_negativity'] > 0.5)
        self.assertTrue(classification['source_sentiment'] < 0.5)

if __name__ == '__main__':
    unittest.main()
