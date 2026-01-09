import asyncio
from pathlib import Path

from project.application.use_cases.load_init_page import FirstPageLoadCategoryUseCase
from project.application.use_cases.restore_paginator import RecoveryProcessedDataCategoryUseCase
from project.application.use_cases.scrape_catalog_use_case import ScrapeCatalogUseCase
from project.application.use_cases.scrape_page import ScrapeAllProductsFromPageUseCase

from project.domain.services.ProcessedPagesService import ProcessedPagesService
from project.domain.services.page_type_detector import PageTypeDetector
from project.domain.value_objects.html_obj import UrlParts

from project.config import CATEGORIES, SUBCATEGORIES
from project.infrastructure.factories.paginator_factory import PaginatorFactory
from project.infrastructure.mappers.ProductMapper import ProductMapper
from project.infrastructure.parsers.ProductsExtractorFromHtml import ProductsExtractorFromHtml
from project.infrastructure.persistence.PgProcessedPagesRepository import PgProcessedPagesRepository
from project.infrastructure.playwright.playwright_page_loader import PlaywrightPageLoader
from project.infrastructure.playwright.cookies_manager import CookiesManager


async def main():
    url = "https://lemanapro.ru/catalogue/oboi-pod-pokrasku"

    root = Path(__file__).resolve().parent
    path_cookies = root / "project" / "infrastructure" / "cookies.txt"
    path_cache = root / "project" / "infrastructure" / "cache" / "cache.txt"

    cookie_provider = CookiesManager(path_cookies)
    cookies = cookie_provider.build()

    detector = PageTypeDetector(CATEGORIES, SUBCATEGORIES)
    parts = UrlParts.from_url(url)
    loader = PlaywrightPageLoader(cookies=cookies)

    # repo = FakePageStateRepository(path_cache)
    # service = PageStateService(repository=repo)
    page_state_repo = PgProcessedPagesRepository()
    page_state_service = ProcessedPagesService(repository=page_state_repo)

    extractor = ProductsExtractorFromHtml()
    mapper = ProductMapper()

    scrape_page_uc = ScrapeAllProductsFromPageUseCase(loader, extractor, mapper)

    if detector.detect(parts).name == "SUBCATEGORY":
        scraper = ScrapeCatalogUseCase(
            loader=loader,
            extractor=extractor,
            mapper=mapper,
            paginator_factory=PaginatorFactory,
            page_state_service=page_state_service,
            first_page_load_category_uc=FirstPageLoadCategoryUseCase,
            recovery_processed_data_category_uc=RecoveryProcessedDataCategoryUseCase,
            scraper_page_uc=scrape_page_uc,
            url_parts=UrlParts,
        )

        async for entities in scraper.execute(url):
            print(entities[:3])

        await loader.close()


if __name__ == "__main__":
    asyncio.run(main())
