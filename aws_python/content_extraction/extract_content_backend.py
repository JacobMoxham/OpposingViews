from abc import ABC, abstractmethod


class ExtractContentBackend(ABC):

    """
       Defines the interface for the extract content backends
    """
    def __init__(self):
        self.backend_name = NotImplementedError

    @abstractmethod
    def extract_content(self, url):
        pass
