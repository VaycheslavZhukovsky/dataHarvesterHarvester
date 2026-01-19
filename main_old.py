import asyncio
from pathlib import Path

from project.application.retry_policy import RetryPolicy
from project.application.use_cases.FirstPageLoadCategoryUseCase import FirstPageLoadCategoryUseCase
from project.application.use_cases.RecoveryProcessedDataCategoryUseCase import RecoveryProcessedDataCategoryUseCase
from project.application.use_cases.ScrapeCatalogUseCase_old import ScrapeCatalogUseCase
from project.application.use_cases.ScrapeAllProductsFromPageUseCase import ScrapeAllProductsFromPageUseCase

from project.domain.services.ProcessedPagesService import ProcessedPagesService
from project.domain.services.PageTypeDetector import PageTypeDetector
from project.domain.value_objects.UrlParts import UrlParts

from project.config import CATEGORIES, SUBCATEGORIES, PROXY
from project.infrastructure.factories.PaginatorFactory import PaginatorFactory
from project.infrastructure.mappers.ProductMapper import ProductMapper
from project.infrastructure.parsers.ProductsExtractorFromHtml import ProductsExtractorFromHtml
from project.infrastructure.persistence.PgCategoryTotalProductsRepository import PgCategoryTotalProductsRepository
from project.infrastructure.persistence.PgProcessedPagesRepository import PgProcessedPagesRepository
from project.infrastructure.persistence.PgProductsRepository import PgProductsRepository
from project.infrastructure.playwright.PlaywrightPageLoader import PlaywrightPageLoader
from project.infrastructure.playwright.CookiesManager import CookiesManager
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


async def main():
    url = "https://lemanapro.ru/catalogue/teplyy-vodyanoy-pol"
    proxy = PROXY
    root = Path(__file__).resolve().parent
    path_cookies = root / "project" / "infrastructure" / "cookies.txt"

    cookie_provider = CookiesManager(path_cookies)
    cookies = cookie_provider.build()

    detector = PageTypeDetector(CATEGORIES, SUBCATEGORIES)
    parts = UrlParts.from_url(url)
    loader = PlaywrightPageLoader(cookies=cookies)

    page_state_repo = PgProcessedPagesRepository()
    processed_pages = ProcessedPagesService(repository=page_state_repo)

    extractor = ProductsExtractorFromHtml()
    mapper = ProductMapper()

    scraper_page_uc = ScrapeAllProductsFromPageUseCase(loader, extractor, mapper)

    paginator_factory = PaginatorFactory

    first_page_load_category_uc = FirstPageLoadCategoryUseCase(loader=loader, paginator_factory=paginator_factory)
    recovery_processed_data_category_uc = RecoveryProcessedDataCategoryUseCase(paginator_factory)

    if detector.detect(parts).name == "SUBCATEGORY":
        scraper = ScrapeCatalogUseCase(
            loader=loader,
            processed_pages=processed_pages,
            first_page_load_category_uc=first_page_load_category_uc,
            recovery_processed_data_category_uc=recovery_processed_data_category_uc,
            scraper_page_uc=scraper_page_uc,
            url_parts=UrlParts,
            page_category_total_products=PgCategoryTotalProductsRepository(),
            page_product_repository=PgProductsRepository(),
            retry_policy=RetryPolicy(),
        )

        async for entities in scraper.execute(url):
            print(entities[:3])

if __name__ == "__main__":
    asyncio.run(main())
