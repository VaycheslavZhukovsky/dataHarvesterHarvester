from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context
from alembic.config import Config


BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

PARSER_DIR = BASE_DIR / "parser"
if str(PARSER_DIR) not in sys.path:
    sys.path.append(str(PARSER_DIR))


ALEMBIC_INI = BASE_DIR / "alembic.ini"
config = Config(str(ALEMBIC_INI))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)



from project.infrastructure.persistence.db import metadata  # type: ignore

target_metadata = metadata



def get_url() -> str:
    """Берём URL из alembic.ini."""
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    """Запуск миграций без подключения к БД."""
    url = get_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Синхронный запуск миграций (внутри async)."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Асинхронный запуск миграций."""
    connectable: AsyncEngine = create_async_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_async_migrations())


run_migrations()
