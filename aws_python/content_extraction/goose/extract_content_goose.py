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

    enable_image_fetching : bool
        whether images should be fetched

    timeout : float
        timeout for requests in seconds

    user_agent : string
        the user agent to send with requests

    Return
    ------
    to_return : dict
        dictionary of values for the extracted article
    '''
    def extract_content(self, url, enable_image_fetching=True, timeout=None, user_agent=None):
        options = {'enable_image_fetching': enable_image_fetching}
        if timeout is not None:
            options['http_timeout'] = timeout

        if user_agent is not None:
            options['browser_user_agent'] = user_agent

        g = Goose(options)
        article = g.extract(url=url)
        to_return = {
            'title': article.title,
            'keywords': article.meta_keywords.split(","),
            'url': url,
            'text': article.cleaned_text
        }
        return to_return
