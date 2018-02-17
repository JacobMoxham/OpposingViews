from goose3 import Goose
from content_extraction.extract_content_backend import ExtractContentBackend

class ExtractContentGoose(ExtractContentBackend):

    def __init__(self):
        super().__init__()
        self.backend_name = "Goose content extraction API"

    '''
    Parameters
    ----------
    url : string
        url of web page to extract content from
    Return
    ------
    to_return : dict
        dictionary of values for the extracted article
    '''
    def extract_content(self, url):
        g = Goose({'enable_image_fetching': True})
        article = g.extract(url=url)
        to_return = {
            'title' : article.title,
            'keywords' : article.meta_keywords.split(","),
            'url' : url,
            'text' : article.cleaned_text
        }
        return to_return
