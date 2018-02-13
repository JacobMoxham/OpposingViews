from abc import ABC, abstractmethod


class SimlarArticleBackend(ABC):
    """
    Defines the interface for the similar article finder backends
    """

    def __init__(self):
        self.backend_name: str = NotImplementedError

    @abstractmethod
    def get_similar_for_keywords(self, keywords):
        """
        Format: [{'title':<title>, 'url':<url>}, ...]
        """
        pass
