from pathlib import Path

from project.application.CategoryTotalsUpdater import update_all_totals
from project.application.HtmlAndProductsCollector import HtmlAndProductsCollector
from project.application.LoadedPagesCollector import LoadedPagesCollector
from project.domain.services.ProcessedPagesRepositoryService import ProcessedPagesRepositoryService
from project.domain.services.number_of_products_extractor import get_number_of_products
from project.domain.value_objects.UrlParts import UrlParts

from project.infrastructure.factories.PaginatorFactory import PaginatorFactory
from project.infrastructure.persistence.PgCategoryTotalProductsRepository import PgCategoryTotalProductsRepository
from project.infrastructure.persistence.PgProcessedPagesRepository import PgProcessedPagesRepository
from project.infrastructure.playwright.PlaywrightPageLoader import PlaywrightPageLoader
from project.infrastructure.playwright.CookiesManager import CookiesManager
from project.infrastructure.logging.logger_config import setup_logger
from test import SUBCATEGORIES

logger = setup_logger(__name__)


class InitialDataLoader:
    """
    Facade/Bootstrapper.
    Responsible for the initial loading of data into the database.
    Runs once when the application starts.
    """

    def __init__(self, subdomain: str = ""):
        root = Path(__file__).resolve().parent.parent.parent
        self.path_cookies = root / "infrastructure" / "cookies.txt"
        self.subdomain = subdomain
        self.cookie_provider = CookiesManager(self.path_cookies)
        self.cookies = self.cookie_provider.build()

        self.loader = PlaywrightPageLoader(cookies=self.cookies)

        self.page_state_repo = PgProcessedPagesRepository()
        self.processed_pages = ProcessedPagesRepositoryService(repository=self.page_state_repo)

        self.paginator_factory = PaginatorFactory

        self.urls = [
            f"https://{self.subdomain}lemanapro.ru/catalogue/{url}"
            for url in SUBCATEGORIES
        ]
        self.url_parts_list = [UrlParts.from_url(url) for url in self.urls]

    async def run(self, limit_pages: int):
        logger.info("InitialDataLoader: data loading started")

        collector = LoadedPagesCollector(self.processed_pages)
        urls_with_pages, urls_without_pages = await collector.collect(self.url_parts_list)

        await self.loader.start()

        collector_html = HtmlAndProductsCollector(
            loader=self.loader,
            paginator_factory=self.paginator_factory,
            data_extractor=get_number_of_products,
            max_workers=limit_pages
        )

        url_parts_list = urls_without_pages[:limit_pages]
        paginators, totals = await collector_html.process(url_parts_list)

        page_category_total_products = PgCategoryTotalProductsRepository()

        for parts, total in totals.items():
            logger.debug(f"{parts}: {total}")

        for parts, paginator in paginators.items():
            logger.debug(f"{parts}: {paginator}")

        await self.loader.close()
        await update_all_totals(page_category_total_products, paginators)

        logger.info("InitialDataLoader: Loading complete.")
