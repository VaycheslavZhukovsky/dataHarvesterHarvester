from abc import ABC, abstractmethod

from project.domain.value_objects.html_obj import UrlParts


class PageHandler(ABC):
    @abstractmethod
    def handle(self, parts: UrlParts):
        ...
