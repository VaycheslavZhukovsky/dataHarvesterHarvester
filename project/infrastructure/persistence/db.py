from __future__ import annotations

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    BigInteger,
    Integer,
    Text,
    Numeric,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from sqlalchemy.sql import func
import os

metadata = MetaData()

categories = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("slug", Text, unique=True, nullable=False),
    Column("total_products", Integer, nullable=True),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)


products = Table(
    "products",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id")),
    Column("displayed_name", Text),
    Column("brand", Text),
    Column("price_main", Numeric),
    Column("price_prev", Numeric),
    Column("currency", Text),
    Column("uom", Text),
    Column("uom_rus", Text),
    Column("additional_price", Numeric),
    Column("additional_uom", Text),
    Column("discount_percent", Numeric),
    Column("step", Integer),
    Column("source", Text),
    Column("width", Numeric),
    Column("m2_per_box", Numeric),
    Column("family_id", Text),
    Column("compare_name", Text),
    Column("link", Text),
    Column("photo_mobile", Text),
    Column("photo_tablet", Text),
    Column("photo_desktop", Text),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)


product_characteristics = Table(
    "product_characteristics",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("product_id", BigInteger, ForeignKey("products.id")),
    Column("key", Text),
    Column("description", Text),
    Column("value", Text),
)


processed_pages = Table(
    "processed_pages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id")),
    Column("page_number", Integer),
    Column("processed_at", DateTime, server_default=func.now()),
)


def _get_database_url() -> str:
    """
    We take the URL from the environment variable or use the default one.
    """
    return os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://parser:parser@localhost:4444/parser_db",
    )


engine: AsyncEngine = create_async_engine(
    _get_database_url(),
    echo=False,
    future=True,
)

session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncSession:
    """
    An asynchronous context manager for working with databases.
    Example:
        async with get_session() as session:
            ...
    """
    async with session_factory() as session:
        yield session
