from newspaper import Article
import nltk
from content_extraction.extract_content_backend import ExtractContentBackend


class ExtractContentNewspaper(ExtractContentBackend):
    def __init__(self):
        super().__init__()
        self.backend_name = "Goose content extraction API"
        nltk.download('punkt')

    '''
    Parameters
    ----------
    url : string
        url of web page to extract content from
    ------
    to_return : dict
        dictionary of values for the extracted article
    '''

    def extract_content(self, url, enable_image_fetching=False, timeout=None, user_agent=None):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        to_return = {
            'title': article.title,
            'keywords': article.keywords,
            'url': url,
            'text': article.text,
            'date': article.publish_date  # yyyy-mm-dd hh:mm:ss
        }
        return to_return
