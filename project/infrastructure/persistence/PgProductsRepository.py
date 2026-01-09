from __future__ import annotations

from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError

from project.domain.entities.Product import Product
from project.infrastructure.exceptions.db_exceptions import CategoryNotFoundError, DatabaseOperationError
from project.infrastructure.persistence.db import (
    session_factory,
    products,
    categories,
)
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class PgProductsRepository:
    """
    Массовая вставка Product агрегатов.
    Гарантирует отсутствие ошибок по primary key.
    """

    async def add_products_bulk(self, slug: str, items: list[Product]) -> None:
        if not items:
            logger.debug(f"Нет продуктов для вставки для slug='{slug}'")
            return

        logger.info(f"Начинаю массовую вставку продуктов для slug='{slug}'")

        try:
            async with session_factory() as session:

                # 0. Получаем category_id по slug
                logger.debug(f"Получаю category_id по slug='{slug}'")
                result = await session.execute(
                    select(categories.c.id).where(categories.c.slug == slug)
                )
                row = result.fetchone()

                if not row:
                    logger.warning(f"Категория slug='{slug}' не найдена")
                    raise CategoryNotFoundError(f"Категория '{slug}' не найдена")

                category_id = row[0]
                logger.debug(f"Найдена категория id={category_id} для slug='{slug}'")

                # 1. Собираем все product_id из агрегатов
                incoming_ids = [int(p.product_id.id) for p in items]
                logger.debug(f"Входящие product_id: {incoming_ids}")

                # 2. Получаем существующие ID одним запросом
                result = await session.execute(
                    select(products.c.id).where(products.c.id.in_(incoming_ids))
                )
                existing_ids = {row[0] for row in result.fetchall()}
                logger.debug(f"Существующие product_id в БД: {existing_ids}")

                # 3. Фильтруем только новые продукты
                new_products = [
                    p for p in items
                    if p.product_id.id not in existing_ids
                ]

                if not new_products:
                    logger.info(f"Все продукты для slug='{slug}' уже существуют")
                    return

                logger.info(f"Новых продуктов для вставки: {len(new_products)}")

                # 4. Преобразуем агрегаты в dict
                rows = [self._to_row(p, category_id) for p in new_products]

                # 5. Массовая вставка
                stmt = insert(products)
                await session.execute(stmt, rows)
                await session.commit()

                logger.info(
                    f"Успешно вставлено {len(new_products)} продуктов для slug='{slug}'"
                )

        except CategoryNotFoundError:
            # Это бизнес‑ошибка — пробрасываем без логирования
            raise

        except SQLAlchemyError as exc:
            logger.exception(
                f"Ошибка SQL при массовой вставке продуктов для slug='{slug}'"
            )
            raise DatabaseOperationError(
                f"Ошибка при массовой вставке продуктов для категории '{slug}'"
            ) from exc

        except Exception as exc:
            logger.exception(
                f"Неизвестная ошибка при массовой вставке продуктов для slug='{slug}'"
            )
            raise DatabaseOperationError(
                f"Неизвестная ошибка при массовой вставке продуктов для категории '{slug}'"
            ) from exc

    def _to_row(self, p: Product, category_id: int) -> dict:
        """
        Маппинг агрегата Product → dict для таблицы products.
        category_id передаётся извне.
        """
        return {
            "id": int(p.product_id.id),
            "category_id": category_id,
            "displayed_name": p.displayed_name.name,
            "brand": p.brand.name,
            "price_main": p.price.main_price,
            "price_prev": p.price.previous_additional_price,
            "currency": p.price.currency,
            "uom": p.price.main_uom,
            "uom_rus": p.price.main_uom_rus,
            "additional_price": p.price.additional_price,
            "additional_uom": p.price.additional_uom,
            "discount_percent": p.price.discount_percent,
            "step": p.price.step,
            "source": p.source.name,
            "width": p.measurement_data.width,
            "m2_per_box": p.measurement_data.m2_per_box,
            "family_id": p.compare_category.family_id,
            "compare_name": p.compare_category.name,
            "link": p.product_link.link,
            "photo_mobile": p.media_main_photo.mobile,
            "photo_tablet": p.media_main_photo.tablet,
            "photo_desktop": p.media_main_photo.desktop,
        }
