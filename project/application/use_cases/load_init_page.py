from project.domain.services.number_of_products_extractor import get_number_of_products
from project.domain.services.url_paginator import UrlPaginator


class FirstPageLoadCategoryUseCase:
    def __init__(self, loader, paginator_factory):
        self.loader = loader
        self.paginator_factory = paginator_factory

    async def get_total_products(self, url: str) -> UrlPaginator:
        html = await self.loader.load_dom(url)
        total_products = get_number_of_products(html)

        return self.paginator_factory.create_paginator(url, total_products)
