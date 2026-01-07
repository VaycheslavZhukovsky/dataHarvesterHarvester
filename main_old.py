import asyncio
from pathlib import Path

from project.application.use_cases.load_init_page import LoadInitialPageUseCase
from project.application.use_cases.restore_paginator import RestorePaginatorUseCase
from project.application.use_cases.scrape_catalog_use_case import ScrapeCatalogUseCase
from project.application.use_cases.scrape_single_page import ScrapeSinglePageUseCase

from project.domain.services.PageStateService import PageStateService
from project.domain.services.page_type_detector import PageTypeDetector
from project.domain.value_objects.html_obj import UrlParts

from project.config import CATEGORIES, SUBCATEGORIES
from project.infrastructure.factories.paginator_factory import PaginatorFactory
from project.infrastructure.mappers.ProductMapper import ProductMapper
from project.infrastructure.parsers.products_extractor import ProductsExtractor
from project.infrastructure.persistence.PgPageStateRepository import PgPageStateRepository
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
    page_state_repo = PgPageStateRepository()
    page_state_service = PageStateService(repository=page_state_repo)

    extractor = ProductsExtractor()
    mapper = ProductMapper()

    scrape_page_uc = ScrapeSinglePageUseCase(loader, extractor, mapper)

    if detector.detect(parts).name == "SUBCATEGORY":
        scraper = ScrapeCatalogUseCase(
            loader=loader,
            extractor=extractor,
            mapper=mapper,
            paginator_factory=PaginatorFactory,
            page_state_service=page_state_service,
            load_initial_uc=LoadInitialPageUseCase,
            restore_paginator_uc=RestorePaginatorUseCase,
            scrape_page_uc=scrape_page_uc,
            url_parts=UrlParts,
        )

        async for entities in scraper.execute(url):
            print(entities[:3])

        await loader.close()


if __name__ == "__main__":
    asyncio.run(main())
