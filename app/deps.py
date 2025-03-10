from collections.abc import AsyncIterator

from asyncpg import connect, Connection
from fastapi import Depends

from app.config import Config, get_config


async def get_db_connection(
    config: Config = Depends(get_config),
) -> AsyncIterator[Connection]:
    conn = await connect(config.DB_DSN)

    try:
        yield conn
    finally:
        await conn.close()
