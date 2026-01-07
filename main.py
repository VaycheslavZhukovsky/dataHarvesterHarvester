import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from project.infrastructure.persistence.db import _get_database_url, metadata


async def create_tables():
    engine = create_async_engine(_get_database_url(), echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
