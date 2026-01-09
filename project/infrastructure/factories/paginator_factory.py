from typing import Optional

from project.domain.services.url_paginator import UrlPaginator
from project.domain.value_objects.html_obj import UrlParts
from project.domain.value_objects.page_state import PageProcessingState


class PaginatorFactory:
    @staticmethod
    def create_paginator(url: str, total_products: Optional[int] = None) -> UrlPaginator:
        parts = UrlParts.from_url(url)
        total_pages = max(1, total_products // 30)
        state = PageProcessingState(total_pages=total_pages)

        return UrlPaginator(parts=parts, state=state, total_products=total_products)
