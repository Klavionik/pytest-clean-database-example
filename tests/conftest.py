from collections.abc import AsyncIterator


from asyncpg import connect, Connection
import pytest
from httpx import AsyncClient, ASGITransport

from app.db import init_db
from app.main import create_app
from app.config import get_config, Config


@pytest.fixture(scope="session")
async def test_database() -> AsyncIterator[None]:
    conn = await connect("postgresql://postgres:password@0.0.0.0:5432/postgres")
    await conn.execute("DROP DATABASE IF EXISTS test;")
    await conn.execute("CREATE DATABASE test;")

    yield

    # await conn.execute("DROP DATABASE test;")


@pytest.fixture(scope="session")
async def test_connection(test_database: None) -> AsyncIterator[Connection]:
    conn = await connect("postgresql://postgres:password@0.0.0.0:5432/test")
    yield conn
    await conn.close()


@pytest.fixture(scope="session")
async def test_tables(test_connection: Connection) -> None:
    await init_db(test_connection)


@pytest.fixture(scope="session")
async def test_client(test_tables: None) -> AsyncIterator[AsyncClient]:
    app = create_app()
    app.dependency_overrides[get_config] = lambda: Config(DB_DSN="postgresql://postgres:password@0.0.0.0:5432/test")

    async with AsyncClient(base_url="http://app", transport=ASGITransport(app=app)) as client:
        yield client


def clean_db_urls(test_tables: None) -> list[str]:
    return [
        "postgresql://postgres:password@0.0.0.0:5432/test",
    ]
