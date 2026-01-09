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
    Обновляет total_products категории.
    Работает через category_id, который ищется по slug.
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
        Обновляет total_products.
        Если категории нет — ничего не делаем.
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
