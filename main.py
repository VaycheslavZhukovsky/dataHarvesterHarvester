from project.application.use_cases.scrape_page_use_case import ScrapePageUseCase
from project.domain.services.the_number_of_products_extractor import get_the_number_of_products
from project.infrastructure.factories.paginator_factory import PaginatorFactory
from project.infrastructure.mappers.product_mapper import ProductMapper
from project.domain.services.products_extractor import ProductsExtractor
from project.infrastructure.playwright.playwright_page_loader import PlaywrightPageLoader


async def main():
    url = "https://lemanapro.ru/catalogue/oboi-pod-pokrasku/"
    root = Path(__file__).resolve().parent.parent
    path_to_the_cache = root / "dataHarvester" / "project" / "infrastructure" / "cookies.txt"

    cookie_provider = CookiesManager(path_to_the_cache)
    cookies = cookie_provider.build()

    loader = PlaywrightPageLoader(cookies=cookies)

    await loader.start()
    html = await loader.load_dom(url=url, timeout=80000)
    await loader.close()
    number = get_the_number_of_products(html)
    print(number)

    paginator = PaginatorFactory.create(url, total_pages=number)
    extractor = ProductsExtractor()
    mapper = ProductMapper()
    while paginator.next_url():
        use_case = ScrapePageUseCase(
            paginator=paginator,
            loader=loader,
            extractor=extractor,
            mapper=mapper,
        )

        entities, paginator = await use_case.execute()
        for entity in entities:
            print(entity)
    print("Next URL:", paginator.next_url())


if __name__ == "__main__":

    import asyncio
    from pathlib import Path

    from project.infrastructure.playwright.cookies_manager import CookiesManager

    asyncio.run(main())
