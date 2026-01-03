from project.application.use_cases.scrape_page_use_case import ScrapeCatalogUseCase
from project.domain.services.page_type_detector import PageTypeDetector
from project.domain.value_objects.html_obj import UrlParts
from project.infrastructure.config import CATEGORIES, SUBCATEGORIES
from project.infrastructure.factories.paginator_factory import PaginatorFactory
from project.infrastructure.mappers.product_mapper import ProductMapper
from project.domain.services.products_extractor import ProductsExtractor
from project.infrastructure.playwright.playwright_page_loader import PlaywrightPageLoader


async def main():
    url = "https://lemanapro.ru/catalogue/oboi-pod-pokrasku/"
    root = Path(__file__).resolve().parent.parent
    path_cookies = root / "dataHarvester" / "project" / "infrastructure" / "cookies.txt"
    cookie_provider = CookiesManager(path_cookies)
    cookies = cookie_provider.build()

    detector = PageTypeDetector(CATEGORIES, SUBCATEGORIES)
    parts = UrlParts.from_url(url)

    if detector.detect(parts).name == "SUBCATEGORY":
        scraper = ScrapeCatalogUseCase(
            loader=PlaywrightPageLoader(cookies=cookies),
            extractor=ProductsExtractor(),
            mapper=ProductMapper(),
            paginator_factory=PaginatorFactory,
        )

        async for entities in scraper.execute(url):
            print(entities[:3])


if __name__ == "__main__":

    import asyncio
    from pathlib import Path

    from project.infrastructure.playwright.cookies_manager import CookiesManager

    asyncio.run(main())
