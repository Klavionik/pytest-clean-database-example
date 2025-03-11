from __future__ import annotations

from collections.abc import AsyncIterator

from mysql.connector.aio import MySQLConnectionAbstract as Connection, connect
from fastapi import Depends

from app.config import Config, get_config
from app.db import mysql_dsn_to_args


async def get_db_connection(
    config: Config = Depends(get_config),
) -> AsyncIterator[Connection]:
    conn = await connect(**mysql_dsn_to_args(config.DB_DSN))

    try:
        yield conn
    finally:
        await conn.close()
