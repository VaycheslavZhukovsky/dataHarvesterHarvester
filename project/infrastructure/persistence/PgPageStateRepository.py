from __future__ import annotations

from typing import Tuple, Optional
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from project.domain.repositories.IPageStateRepository import IPageStateRepository
from project.infrastructure.exceptions.db_exceptions import DatabaseOperationError, CategoryNotFoundError, \
    DatabaseConnectionError
from project.infrastructure.persistence.db import (
    session_factory,
    processed_pages,
    categories,
)
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class PgPageStateRepository(IPageStateRepository):
    """
    Хранит обработанные страницы категории.
    Работает через category_id, который ищется по slug.
    """
    async def _find_category_id(self, slug: str) -> Optional[int]:
        logger.debug(f"Поиск category_id по slug='{slug}'")

        try:
            async with session_factory() as session:
                result = await session.execute(
                    select(categories.c.id).where(categories.c.slug == slug)
                )
                row = result.fetchone()

        except ConnectionRefusedError as exc:
            logger.exception("Ошибка подключения к БД")
            raise DatabaseConnectionError("Ошибка подключения к БД") from exc

        except Exception as exc:
            logger.exception(f"Ошибка при поиске категории slug='{slug}'")
            raise DatabaseOperationError(
                f"Ошибка при поиске категории '{slug}'"
            ) from exc

        if row:
            logger.debug(f"Найдена категория: id={row[0]} для slug='{slug}'")
            return row[0]

        return None

    async def add_url(self, slug: str, page: int) -> None:
        """
        Добавляет обработанную страницу категории.
        Если категории нет — выбрасываем исключение.
        """

        logger.info(f"Добавление обработанной страницы page={page} для slug='{slug}'")

        category_id = await self._find_category_id(slug)
        if category_id is None:
            raise CategoryNotFoundError(f"Категория '{slug}' не найдена")

        try:
            async with session_factory() as session:
                stmt = (
                    pg_insert(processed_pages)
                    .values(category_id=category_id, page_number=page)
                    .on_conflict_do_nothing()
                )
                await session.execute(stmt)
                await session.commit()
        except Exception as exc:
            logger.exception(
                f"Ошибка при добавлении страницы page={page} для slug='{slug}'"
            )
            raise DatabaseOperationError(
                f"Ошибка при добавлении обработанной страницы '{slug}', page={page}"
            ) from exc

        logger.info(
            f"Страница page={page} успешно добавлена для категории slug='{slug}'"
        )

    async def get_data_from_category(self, slug: str) -> Tuple[int, Tuple[int, ...]]:
        """
        Возвращает:
        - total_products
        - tuple(processed_pages)
        Если категории нет — возвращает (0, ()).
        """

        logger.debug(f"Получение данных категории slug='{slug}'")

        category_id = await self._find_category_id(slug)

        try:
            async with session_factory() as session:
                result = await session.execute(
                    select(categories.c.total_products).where(categories.c.id == category_id)
                )
                total_products = result.scalar() or 0

                rows = await session.execute(
                    select(processed_pages.c.page_number).where(
                        processed_pages.c.category_id == category_id
                    )
                )
                pages = sorted({r[0] for r in rows})
        except Exception as exc:
            logger.exception(
                f"Ошибка при получении данных категории slug='{slug}'"
            )
            raise DatabaseOperationError(
                f"Ошибка при получении данных категории '{slug}'"
            ) from exc

        logger.debug(
            f"Для slug='{slug}' найдено total_products={total_products}, "
            f"processed_pages={pages}"
        )

        return total_products, tuple(pages)
