from typing import Protocol

from project.domain.entities.Product import Product


class IProductRepository(Protocol):
    async def save_many(self, products: list[Product]) -> None: ...
