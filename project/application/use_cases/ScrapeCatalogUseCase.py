from __future__ import annotations

from typing import List

from project.domain.entities.Product import Product
from project.domain.interfaces import IProductRepository
from project.domain.interfaces.IProductsExtractor import IProductsExtractor
from project.domain.repositories.IPageStateRepository import IPageStateRepository
from project.domain.interfaces.IPageLoader import IPageLoader
from project.infrastructure.mappers.ProductMapper import ProductMapper
from project.domain.services.url_paginator import UrlPaginator
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class ScrapeCatalogUseCase:
    """
    Загружает страницу каталога, парсит продукты, сохраняет в БД,
    обновляет состояние пагинации.
    """

    def __init__(
            self,
            paginator: UrlPaginator,
            loader: IPageLoader,
            extractor: IProductsExtractor,
            mapper: ProductMapper,
            product_repo: IProductRepository,
            page_state_repo: IPageStateRepository,
    ):
        self.paginator = paginator
        self.loader = loader
        self.extractor = extractor
        self.mapper = mapper
        self.product_repo = product_repo
        self.page_state_repo = page_state_repo

    async def execute(self) -> List[Product]:
        url = self.paginator.next_url()
        logger.info(f"Starting catalog scraping for URL: {url}")
        if not url:
            return []

        # -----------------------------
        # 1. Загрузка HTML
        # -----------------------------
        await self.loader.start()
        html = await self.loader.load_dom(url=url)
        await self.loader.close()

        # -----------------------------
        # 2. Парсинг
        # -----------------------------
        raw_products = self.extractor.create_products_list_from_str(html)
        entities = self.mapper.to_entities(raw_products)

        # -----------------------------
        # 3. Сохранение в БД
        # -----------------------------
        await self.product_repo.save_many(entities)

        # -----------------------------
        # 4. Обновление состояния пагинации
        # -----------------------------
        await self.page_state_repo.add_url(url)
        self.paginator = self.paginator.mark_processed()

        return entities
