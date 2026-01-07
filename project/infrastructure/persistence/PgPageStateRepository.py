from __future__ import annotations

from typing import Tuple
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from project.domain.repositories.IPageStateRepository import IPageStateRepository
from project.infrastructure.persistence.db import (
    session_factory,
    processed_pages,
    categories,
)


class PgPageStateRepository(IPageStateRepository):
    """
    Хранит обработанные страницы категории.
    Работает через category_id, который ищется по slug.
    """

    async def _find_category_id(self, slug: str) -> int | None:
        async with session_factory() as session:
            result = await session.execute(
                select(categories.c.id).where(categories.c.slug == slug)
            )
            row = result.fetchone()
            return row[0] if row else None

    async def add_url(self, slug: str, page: int) -> None:
        """
        Добавляет обработанную страницу категории.
        Если категории нет — ничего не делаем.
        """

        category_id = await self._find_category_id(slug)
        if category_id is None:
            # Категория ещё не создана — пропускаем
            return

        async with session_factory() as session:
            stmt = (
                pg_insert(processed_pages)
                .values(
                    category_id=category_id,
                    page_number=page,
                )
                .on_conflict_do_nothing()
            )
            await session.execute(stmt)
            await session.commit()

    async def get_data_from_category(self, slug: str) -> Tuple[int, Tuple[int, ...]]:
        """
        Возвращает:
        - total_products
        - tuple(processed_pages)
        Если категории нет — возвращает (0, ()).
        """
        category_id = await self._find_category_id(slug)

        if category_id is None:
            return 0, ()

        async with session_factory() as session:
            # total_products
            result = await session.execute(
                select(categories.c.total_products).where(categories.c.id == category_id)
            )
            total_products = result.scalar() or 0

            # processed pages
            rows = await session.execute(
                select(processed_pages.c.page_number).where(
                    processed_pages.c.category_id == category_id
                )
            )
            pages = sorted({r[0] for r in rows})

        return total_products, tuple(pages)
