from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


PARSER_DIR = BASE_DIR / "parser"
if str(PARSER_DIR) not in sys.path:
    sys.path.append(str(PARSER_DIR))

from project.infrastructure.persistence.db import metadata  # type: ignore

target_metadata = metadata


def get_url() -> str:
    """
    Берём URL из alembic.ini.
    """
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    """
    Запуск миграций в offline-режиме (генерация SQL без подключения).
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Запуск миграций в online-режиме (с подключением к БД).
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Асинхронный запуск миграций.
    """
    connectable: AsyncEngine = create_async_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Определяем, offline или online режим.
    """
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_async_migrations())


run_migrations_online()
