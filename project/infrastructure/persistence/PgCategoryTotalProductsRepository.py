from __future__ import annotations

from sqlalchemy import select, update

from project.domain.repositories.ICategoryTotalProductsRepository import (
    ICategoryTotalProductsRepository,
)
from project.infrastructure.persistence.db import (
    session_factory,
    categories,
)


class PgCategoryTotalProductsRepository(ICategoryTotalProductsRepository):
    """
    Updates the total_products count for a category.
    It works using the category_id, which is found by its slug.
    """

    async def _find_category_id(self, slug: str) -> int | None:
        async with session_factory() as session:
            result = await session.execute(
                select(categories.c.id).where(categories.c.slug == slug)
            )
            row = result.fetchone()
            return row[0] if row else None

    async def update_total_products(self, slug: str, total: int) -> None:
        """
        Updates total_products.
        If the category does not exist, we do nothing.
        """

        category_id = await self._find_category_id(slug)
        if category_id is None:
            return

        async with session_factory() as session:
            stmt = (
                update(categories)
                .where(categories.c.id == category_id)
                .values(total_products=total)
            )
            await session.execute(stmt)
            await session.commit()
