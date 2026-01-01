from typing import Optional

from project.domain.services.url_paginator import UrlPaginator
from project.domain.value_objects.html_obj import UrlParts
from project.domain.value_objects.page_state import PageProcessingState


class PaginatorFactory:
    @staticmethod
    def create(url: str, total_pages: Optional[int] = None) -> UrlPaginator:
        parts = UrlParts.from_url(url)
        state = PageProcessingState(total_pages=total_pages)
        return UrlPaginator(parts=parts, state=state)
