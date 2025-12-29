from typing import Protocol

from project.domain.entities.product import Product


class ProductRepository(Protocol):

    def list(self) -> list[Product]:
        pass
