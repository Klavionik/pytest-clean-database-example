from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator

from fastapi import FastAPI
from app.api import router
from app.db import init_db, mysql_dsn_to_args
from app.config import get_config
from mysql.connector.aio import connect


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    config = get_config()
    async with await connect(**mysql_dsn_to_args(config.DB_DSN)) as conn:
        await init_db(conn)

    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app
