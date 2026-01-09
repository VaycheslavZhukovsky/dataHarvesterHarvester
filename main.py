import asyncio
from pathlib import Path

from project.application.retry_policy import RetryPolicy
from project.application.use_cases.load_init_page import LoadInitialPageUseCase
from project.application.use_cases.restore_paginator import RestorePaginatorUseCase
from project.application.use_cases.scrape_catalog_use_case import ScrapeCatalogUseCase
from project.application.use_cases.scrape_page import ScrapeAllProductsFromPageUseCase

from project.domain.services.PageStateService import PageStateService
from project.domain.services.page_type_detector import PageTypeDetector
from project.domain.value_objects.html_obj import UrlParts

from project.config import CATEGORIES, SUBCATEGORIES
from project.infrastructure.factories.paginator_factory import PaginatorFactory
from project.infrastructure.mappers.ProductMapper import ProductMapper
from project.infrastructure.parsers.products_extractor import ProductsExtractor
from project.infrastructure.persistence.PgCategoryTotalProductsRepository import PgCategoryTotalProductsRepository
from project.infrastructure.persistence.PgPageStateRepository import PgPageStateRepository
from project.infrastructure.persistence.PgProductsRepository import PgProductsRepository
from project.infrastructure.playwright.playwright_page_loader import PlaywrightPageLoader
from project.infrastructure.playwright.cookies_manager import CookiesManager
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


async def main():
    url = "https://lemanapro.ru/catalogue/professionalnye-instrumenty-i-krepezh"

    root = Path(__file__).resolve().parent
    path_cookies = root / "project" / "infrastructure" / "cookies.txt"

    cookie_provider = CookiesManager(path_cookies)
    cookies = cookie_provider.build()

    detector = PageTypeDetector(CATEGORIES, SUBCATEGORIES)
    parts = UrlParts.from_url(url)
    loader = PlaywrightPageLoader(cookies=cookies)

    page_state_repo = PgPageStateRepository()
    page_state_service = PageStateService(repository=page_state_repo)

    extractor = ProductsExtractor()
    mapper = ProductMapper()

    scrape_page_uc = ScrapeAllProductsFromPageUseCase(loader, extractor, mapper)
    paginator_factory = PaginatorFactory
    load_initial_uc = LoadInitialPageUseCase(loader=loader, paginator_factory=paginator_factory)
    restore_paginator_uc = RestorePaginatorUseCase(paginator_factory)

    if detector.detect(parts).name == "SUBCATEGORY":
        scraper = ScrapeCatalogUseCase(
            loader=loader,
            page_state_service=page_state_service,
            load_initial_uc=load_initial_uc,
            restore_paginator_uc=restore_paginator_uc,
            scrape_page_uc=scrape_page_uc,
            url_parts=UrlParts,
            page_category_total_products=PgCategoryTotalProductsRepository(),
            page_product_repository=PgProductsRepository(),
            retry_policy=RetryPolicy(),
        )

        async for entities in scraper.execute(url):
            print(entities[:3])

if __name__ == "__main__":
    asyncio.run(main())
