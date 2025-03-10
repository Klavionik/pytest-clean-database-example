from asyncpg import Connection


async def init_db(conn: Connection) -> None:
    await conn.execute(
        "CREATE TABLE IF NOT EXISTS todos(id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY, owner TEXT UNIQUE, items JSONB);"
    )
