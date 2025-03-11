from __future__ import annotations
from collections.abc import AsyncIterator

from mysql.connector.aio import MySQLConnectionAbstract as Connection, connect
import pytest
from httpx import AsyncClient, ASGITransport

from app.db import init_db, mysql_dsn_to_args
from app.main import create_app
from app.config import get_config, Config


@pytest.fixture(scope="session")
async def test_database() -> AsyncIterator[None]:
    async with await connect(
        **mysql_dsn_to_args("mysql://root:password@0.0.0.0:3306/mysql")
    ) as conn:
        async with await conn.cursor() as cur:
            await cur.execute("DROP DATABASE IF EXISTS test;")
            await cur.execute("CREATE DATABASE test;")

        yield

        async with await conn.cursor() as cur:
            await cur.execute("DROP DATABASE test;")


@pytest.fixture()
async def test_connection(test_database: None) -> AsyncIterator[Connection]:
    async with await connect(
        **mysql_dsn_to_args("mysql://root:password@0.0.0.0:3306/test")
    ) as conn:
        yield conn


@pytest.fixture(scope="session")
async def test_tables(test_database: None) -> None:
    async with await connect(
        **mysql_dsn_to_args("mysql://root:password@0.0.0.0:3306/test")
    ) as conn:
        await init_db(conn)


@pytest.fixture()
async def test_client(test_tables: None) -> AsyncIterator[AsyncClient]:
    app = create_app()

    def get_test_config() -> Config:
        return Config(DB_DSN="mysql://root:password@0.0.0.0:3306/test")

    app.dependency_overrides[get_config] = get_test_config

    async with AsyncClient(
        base_url="http://app", transport=ASGITransport(app)
    ) as client:
        yield client


@pytest.fixture(scope="session")
def clean_db_urls(test_tables: None) -> list[str]:
    return [
        "mysql://root:password@0.0.0.0:3306/test",
    ]
