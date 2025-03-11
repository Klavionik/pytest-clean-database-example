import urllib.parse
from typing import TypedDict

from mysql.connector.aio import MySQLConnectionAbstract as Connection


class MySQLArgs(TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: str
    autocommit: bool


async def init_db(conn: Connection) -> None:
    async with await conn.cursor() as cur:
        await cur.execute(
            "CREATE TABLE IF NOT EXISTS todos(id BIGINT PRIMARY KEY AUTO_INCREMENT, owner VARCHAR(64) UNIQUE, items JSON);"
        )


def mysql_dsn_to_args(dsn: str) -> MySQLArgs:
    url = urllib.parse.urlparse(dsn)

    if (
        url.hostname is None
        or url.port is None
        or url.username is None
        or url.password is None
    ):
        raise ValueError(f"Incorrect MySQL connection string {url}.")

    args = MySQLArgs(
        host=url.hostname,
        port=url.port,
        user=url.username,
        password=url.password,
        database=url.path.lstrip("/"),
        autocommit=True,
    )

    return args
