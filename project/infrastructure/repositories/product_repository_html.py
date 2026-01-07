from pathlib import Path

from project.domain.entities.Product import Product
from project.domain.repositories.IProductRepository import IProductRepository
from project.infrastructure.mappers.ProductMapper import ProductMapper
from project.infrastructure.parsers.products_extractor import ProductsExtractor


class ProductRepositoryHtml(IProductRepository):
    def __init__(self, extractor: ProductsExtractor, mapper: ProductMapper, html_path: Path):
        self.extractor = extractor
        self.mapper = mapper
        self.html_path = html_path

    def list(self) -> list[Product]:
        raw_list = self.extractor.create_products_list(self.html_path)
        return [self.mapper.to_entity(r) for r in raw_list]
