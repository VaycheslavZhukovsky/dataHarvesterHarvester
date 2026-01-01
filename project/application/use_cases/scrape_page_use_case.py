from project.domain.interfaces.page_loader import IPageLoader
from project.domain.interfaces.cookies_manager import ICookieProvider
from project.domain.interfaces.product_extractor import IProductsExtractor
from project.domain.services.url_paginator import UrlPaginator
from project.infrastructure.mappers.product_mapper import ProductMapper


class ScrapePageUseCase:
    """
    Use-case: загрузить страницу, извлечь продукты, преобразовать в сущности,
    обновить состояние пагинации.
    """

    def __init__(
            self,
            paginator: UrlPaginator,
            loader: IPageLoader,
            extractor: IProductsExtractor,
            mapper: ProductMapper,
    ):
        self.paginator = paginator
        self.loader = loader
        self.extractor = extractor
        self.mapper = mapper

    async def execute(self):

        url = self.paginator.next_url()

        await self.loader.start()
        html = await self.loader.load_dom(url=url, timeout=80000)
        await self.loader.close()

        products_raw = self.extractor.create_products_list_from_str(html)

        entities = self.mapper.to_entities(products_raw)

        self.paginator = self.paginator.mark_processed()

        return entities, self.paginator
