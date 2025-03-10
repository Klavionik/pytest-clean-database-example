import contextlib
from collections.abc import AsyncIterator

from fastapi import FastAPI
from app.api import router
from app.db import init_db
from app.config import get_config
from asyncpg import connect


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    config = get_config()
    conn = await connect(config.DB_DSN)
    await init_db(conn)
    await conn.close()
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app
