from pathlib import Path
from itertools import chain

from project.application.LoadedPagesCollector import LoadedPagesCollector
from project.application.use_cases.RecoveryProcessedDataCategoryUseCase import RecoveryProcessedDataCategoryUseCase
from project.application.use_cases.scrape_all import scrape_all

from project.domain.services.ProcessedPagesService import ProcessedPagesService
from project.domain.value_objects.UrlParts import UrlParts

from project.config import PROXY
from project.infrastructure.factories.PaginatorFactory import PaginatorFactory
from project.infrastructure.mappers.ProductMapper import ProductMapper
from project.infrastructure.parsers.ProductsExtractorFromHtml import ProductsExtractorFromHtml
from project.infrastructure.persistence.PgProcessedPagesRepository import PgProcessedPagesRepository
from project.infrastructure.persistence.PgProductsRepository import PgProductsRepository
from project.infrastructure.playwright.PlaywrightPageLoader import PlaywrightPageLoader
from project.infrastructure.playwright.CookiesManager import CookiesManager


class ScraperApp:
    def __init__(self):
        root = Path(__file__).resolve().parent.parent
        path_cookies = root / "infrastructure" / "cookies.txt"

        cookie_provider = CookiesManager(path_cookies)
        cookies = cookie_provider.build()

        self.loader = PlaywrightPageLoader(proxy=PROXY, cookies=cookies)
        self.extractor = ProductsExtractorFromHtml()
        self.mapper = ProductMapper()

        self.page_state_repo = PgProcessedPagesRepository()
        self.processed_pages = ProcessedPagesService(self.page_state_repo)

        self.paginator_factory = PaginatorFactory
        self.recovery_uc = RecoveryProcessedDataCategoryUseCase(self.paginator_factory)

        self.products_repo = PgProductsRepository()

    async def scrape_category(self, category_slug: str, limit_pages: int = 5):
        await self.loader.start()

        url = f"https://lemanapro.ru/catalogue/{category_slug}"
        url_parts = UrlParts.from_url(url)

        collector = LoadedPagesCollector(self.processed_pages)
        urls_with_pages, _ = await collector.collect([url_parts])

        paginators = [
            self.recovery_uc.assemble_paginator(str(url_parts), processed_data[0], processed_data[1])
            for url_parts, processed_data in urls_with_pages
        ]

        paginator = paginators[0]

        urls = []
        for _ in range(limit_pages):
            u = paginator.next_url()
            if not u:
                break
            urls.append(u)
            paginator = paginator.mark_processed()

        results = await scrape_all(urls, self.loader, self.extractor, self.mapper)
        await self.loader.close()

        flat = list(chain.from_iterable(results.values()))
        await self.products_repo.add_products_bulk(slug=category_slug, items=flat)

        return flat
