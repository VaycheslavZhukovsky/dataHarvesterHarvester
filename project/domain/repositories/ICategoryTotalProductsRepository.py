from typing import Protocol


class ICategoryTotalProductsRepository(Protocol):
    async def update_total_products(self, slug: str, total: int) -> None:
        """Updates the total_products count for a category based on its slug."""
        raise NotImplementedError
