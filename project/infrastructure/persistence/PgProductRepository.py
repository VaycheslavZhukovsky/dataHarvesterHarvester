from __future__ import annotations

from typing import List
from sqlalchemy import insert, update, select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from project.domain.entities.Product import Product
from project.domain.repositories.IProductRepository import IProductRepository
from project.infrastructure.persistence.db import (
    session_factory,
    products,
    product_characteristics,
)


class PgProductRepository(IProductRepository):
    """
    Репозиторий продуктов.
    Использует SQLAlchemy Core + async.
    """

    async def save_many(self, items: List[Product]) -> None:
        async with session_factory() as session:
            for product in items:
                # -----------------------------
                # UPSERT в таблицу products
                # -----------------------------
                stmt = pg_insert(products).values(
                    id=int(product.product_id.id),
                    displayed_name=product.displayed_name.name,
                    brand=product.brand.name,
                    category=product.category.category,
                    price_main=product.price.main_price,
                    price_prev=product.price.previous_price,
                    currency=product.price.currency,
                    uom=product.price.main_uom,
                    uom_rus=product.price.main_uom_rus,
                    additional_price=product.price.additional_price,
                    additional_uom=product.price.additional_uom,
                    discount_percent=product.price.discount_percent,
                    step=product.price.step,
                    source=product.source.name,
                    width=product.measurement_data.width,
                    m2_per_box=product.measurement_data.m2_per_box,
                    family_id=product.compare_category.family_id,
                    compare_name=product.compare_category.name,
                    link=product.product_link.link,
                    photo_mobile=product.media_main_photo.mobile,
                    photo_tablet=product.media_main_photo.tablet,
                    photo_desktop=product.media_main_photo.desktop,
                ).on_conflict_do_update(
                    index_elements=[products.c.id],
                    set_={
                        "displayed_name": pg_insert.excluded.displayed_name,
                        "brand": pg_insert.excluded.brand,
                        "category": pg_insert.excluded.category,
                        "price_main": pg_insert.excluded.price_main,
                        "price_prev": pg_insert.excluded.price_prev,
                        "currency": pg_insert.excluded.currency,
                        "uom": pg_insert.excluded.uom,
                        "uom_rus": pg_insert.excluded.uom_rus,
                        "additional_price": pg_insert.excluded.additional_price,
                        "additional_uom": pg_insert.excluded.additional_uom,
                        "discount_percent": pg_insert.excluded.discount_percent,
                        "step": pg_insert.excluded.step,
                        "source": pg_insert.excluded.source,
                        "width": pg_insert.excluded.width,
                        "m2_per_box": pg_insert.excluded.m2_per_box,
                        "family_id": pg_insert.excluded.family_id,
                        "compare_name": pg_insert.excluded.compare_name,
                        "link": pg_insert.excluded.link,
                        "photo_mobile": pg_insert.excluded.photo_mobile,
                        "photo_tablet": pg_insert.excluded.photo_tablet,
                        "photo_desktop": pg_insert.excluded.photo_desktop,
                    },
                )

                await session.execute(stmt)

                # -----------------------------
                # Характеристики (INSERT IGNORE)
                # -----------------------------
                for ch in product.characteristics.characteristics:
                    stmt_char = pg_insert(product_characteristics).values(
                        product_id=int(product.product_id.id),
                        key=ch.key,
                        description=ch.description,
                        value=ch.value,
                    ).on_conflict_do_nothing()

                    await session.execute(stmt_char)

            await session.commit()
