from typing import Protocol

from project.domain.entities.Product import Product


class IProductRepository(Protocol):

    def list(self) -> list[Product]:
        pass
