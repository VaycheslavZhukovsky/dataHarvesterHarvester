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


class PgProcessedPagesRepository(IPageStateRepository):
    """
    Stores processed category pages.
    It works through the category_id, which is found by the slug.
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
            logger.exception("Database connection error")
            raise DatabaseConnectionError("Database connection error") from exc

        except Exception as exc:
            logger.exception(f"Error searching for category with slug='{slug}'")
            raise DatabaseOperationError(
                f"Error searching for category '{slug}'"
            ) from exc

        if row:
            logger.debug(f"Category found: id={row[0]} for slug='{slug}'")
            return row[0]

        return None

    async def add_url(self, slug: str, page: int) -> None:
        """
        Adds the processed category page.
        If the category does not exist, an exception is thrown.
        """

        logger.info(f"Adding processed page page={page} for slug='{slug}'")

        category_id = await self._find_category_id(slug)
        if category_id is None:
            raise CategoryNotFoundError(f"Category '{slug}' not found")

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
                f"Error adding page={page} for slug='{slug}'"
            )
            raise DatabaseOperationError(
                f"Error adding processed page '{slug}', page={page}"
            ) from exc

        logger.info(
            f"Page {page} has been successfully added for category slug='{slug}'."
        )

    async def get_data_from_category(self, slug: str) -> Tuple[int, Tuple[int, ...]]:
        """
        Returns:
            - total_products
            - tuple(processed_pages)
            If the category does not exist, it returns (0, ()).
        """

        logger.debug(f"Retrieving data for category with slug='{slug}'")

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
                f"Error retrieving data for category with slug='{slug}'"
            )
            raise DatabaseOperationError(
                f"Error retrieving data for category '{slug}'"
            ) from exc

        logger.debug(
            f"For slug='{slug}', total_products={total_products} were found, "
            f"processed_pages={pages}"
        )

        return total_products, tuple(pages)
