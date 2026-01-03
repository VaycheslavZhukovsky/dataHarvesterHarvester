from project.domain.handlers.base import PageHandler
from project.domain.value_objects.html_obj import UrlParts


class ProductHandler(PageHandler):
    def handle(self, parts: UrlParts):
        return {
            "type": "product",
            "domain": parts.domain,
            "segments": parts.segments,
            "query": parts.query,
        }
