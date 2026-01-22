import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict

from project.domain.value_objects.UrlParts import UrlParts
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class HtmlAndProductsCollector:
    """
    1. Competitively loads HTML for the list of UrlParts.
    2. Calculates total_products in parallel (CPU).
    3. Creates a paginator for each URL.
    """

    def __init__(self, loader, paginator_factory, data_extractor, max_workers: int):
        self.loader = loader
        self.paginator_factory = paginator_factory
        self.data_extractor = data_extractor
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    async def load_all_html(self, urls: List[UrlParts]) -> Dict[UrlParts, str]:
        """
        Competitively loads HTML.
        """
        tasks = [
            asyncio.create_task(self.loader.load_dom(str(parts)))
            for parts in urls
        ]

        html_list = await asyncio.gather(*tasks)

        return {str(parts): html for parts, html in zip(urls, html_list)}

    async def compute_total_products(self, html_map: Dict[UrlParts, str]) -> Dict[UrlParts, int]:
        """
        It simultaneously calculates total_products using ProcessPoolExecutor.
        """
        loop = asyncio.get_running_loop()

        tasks = [
            loop.run_in_executor(self.executor, self.data_extractor, html)
            for html in html_map.values()
        ]

        totals = await asyncio.gather(*tasks)

        return {parts: total for parts, total in zip(html_map.keys(), totals)}

    async def build_paginators(self, totals: Dict[UrlParts, int]):
        """
        It creates a paginator for each URL.
        """
        paginators = {}

        for parts, total_products in totals.items():
            paginator = self.paginator_factory.create_paginator(str(parts), total_products)
            paginators[parts] = paginator

        return paginators

    async def process(self, urls_without_pages: List[UrlParts]):
        """
        The complete pipeline:
        1. Loading the HTML
        2. CPU processing
        3. Creating the paginator
        """
        logger.debug("Loading HTML...")
        html_map = await self.load_all_html(urls_without_pages)

        logger.debug("Count total_products...")
        totals = await self.compute_total_products(html_map)

        logger.debug("Creating a paginator....")
        paginators = await self.build_paginators(totals)

        return paginators, totals
