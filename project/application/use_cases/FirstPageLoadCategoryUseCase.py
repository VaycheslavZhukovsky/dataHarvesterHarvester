import asyncio
from concurrent.futures import ProcessPoolExecutor

from project.domain.services.number_of_products_extractor import get_number_of_products
from project.domain.services.UrlPaginator import UrlPaginator


class FirstPageLoadCategoryUseCase:
    def __init__(self, loader, paginator_factory, executor: ProcessPoolExecutor):
        self.loader = loader
        self.paginator_factory = paginator_factory
        self.executor = executor

    async def get_total_products(self, url: str) -> UrlPaginator:
        html = await self.loader.load_dom(url)

        loop = asyncio.get_running_loop()
        total_products = await loop.run_in_executor(
            self.executor,
            get_number_of_products,
            html
        )

        return self.paginator_factory.create_paginator(url, total_products)


