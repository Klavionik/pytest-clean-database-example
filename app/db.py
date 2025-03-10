from asyncpg import Connection


async def init_db(conn: Connection) -> None:
    await conn.execute("CREATE TABLE IF NOT EXISTS users(id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY, username TEXT UNIQUE);")
    await conn.execute("CREATE TABLE IF NOT EXISTS todos(id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY, user_id BIGINT REFERENCES users (id), items JSONB);")