from functools import reduce

from project.domain.services.page_state_service import PageStateService
from project.domain.services.the_number_of_products_extractor import get_the_number_of_products
from project.infrastructure.repositories.fake_page_state_repository import FakePageStateRepository


class ScrapeCatalogUseCase:
    def __init__(self, loader, extractor, mapper, paginator_factory):
        self.loader = loader
        self.extractor = extractor
        self.mapper = mapper
        self.paginator_factory = paginator_factory

    async def execute(self, url: str):
        repo = FakePageStateRepository()
        service = PageStateService(repository=repo)
        all_pages, processed = service.get_loaded_pages(url)

        await self.loader.start()
        if not processed:
            html = await self.loader.load_dom(url)
            total_pages = int(get_the_number_of_products(html) / 30)
            paginator = self.paginator_factory.create(url, total_pages)
        else:
            paginator = self.paginator_factory.create(url, all_pages)
            paginator = reduce(lambda acc, i: acc.mark_processed(i), processed, paginator)

        print(paginator)

        while paginator.next_url():
            page_url = paginator.next_url()
            html = await self.loader.load_dom(page_url)

            products_raw = self.extractor.create_products_list_from_str(html)
            entities = self.mapper.to_entities(products_raw)

            paginator = paginator.mark_processed()
            yield entities

        await self.loader.close()
