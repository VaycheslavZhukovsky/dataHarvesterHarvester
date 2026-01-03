from project.domain.handlers.base import PageHandler
from project.domain.value_objects.html_obj import UrlParts


class CategoryHandler(PageHandler):
    def handle(self, parts: UrlParts):
        return {
            "type": "category",
            "domain": parts.domain,
            "segments": parts.segments,
            "query": parts.query,
        }
