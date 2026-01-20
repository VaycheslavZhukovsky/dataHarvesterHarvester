import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict

from project.domain.value_objects.UrlParts import UrlParts
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class HtmlAndProductsCollector:
    """
    1. Конкурентно загружает HTML для списка UrlParts.
    2. Параллельно считает total_products (CPU).
    3. Создаёт paginator для каждого URL.
    """

    def __init__(self, loader, paginator_factory, get_number_of_products, max_workers: int = 4):
        self.loader = loader
        self.paginator_factory = paginator_factory
        self.get_number_of_products = get_number_of_products
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    async def load_all_html(self, urls: List[UrlParts]) -> Dict[UrlParts, str]:
        """
        Конкурентно загружает HTML.
        """
        tasks = [
            asyncio.create_task(self.loader.load_dom(str(parts)))
            for parts in urls
        ]

        html_list = await asyncio.gather(*tasks)

        return {str(parts): html for parts, html in zip(urls, html_list)}

    async def compute_total_products(self, html_map: Dict[UrlParts, str]) -> Dict[UrlParts, int]:
        """
        Параллельно считает total_products в ProcessPoolExecutor.
        """
        loop = asyncio.get_running_loop()

        tasks = [
            loop.run_in_executor(self.executor, self.get_number_of_products, html)
            for html in html_map.values()
        ]

        totals = await asyncio.gather(*tasks)

        return {parts: total for parts, total in zip(html_map.keys(), totals)}

    async def build_paginators(self, totals: Dict[UrlParts, int]):
        """
        Создаёт paginator для каждого URL.
        """
        paginators = {}

        for parts, total_products in totals.items():
            paginator = self.paginator_factory.create_paginator(str(parts), total_products)
            paginators[parts] = paginator

        return paginators

    async def process(self, urls_without_pages: List[UrlParts]):
        """
        Полный pipeline:
        1. загрузка html
        2. CPU обработка
        3. создание paginator
        """
        logger.info("Загружаю HTML...")
        html_map = await self.load_all_html(urls_without_pages)

        logger.info("Считаю total_products...")
        totals = await self.compute_total_products(html_map)

        logger.info("Создаю paginator...")
        paginators = await self.build_paginators(totals)

        return paginators, totals
