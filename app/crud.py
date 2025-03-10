import json

from asyncpg import Connection

from app.models import TodoList


async def list_todos(conn: Connection) -> list[TodoList]:
    rows = await conn.fetch("SELECT id, owner, items FROM todos;")

    return [
        TodoList(id=row["id"], owner=row["owner"], items=json.loads(row["items"]))
        for row in rows
    ]


async def create_todo(owner: str, items: list[str], conn: Connection) -> TodoList:
    row = await conn.fetchrow(
        "INSERT INTO todos (owner, items) VALUES ($1, $2) RETURNING id;",
        owner,
        json.dumps(items),
    )
    assert row is not None
    return TodoList(id=row["id"], owner=owner, items=items)


async def edit_todo(
    todo_id: int, owner: str, items: list[str], conn: Connection
) -> TodoList:
    await conn.execute(
        "UPDATE todos SET owner = $2, items = $3 WHERE id = $1;",
        todo_id,
        owner,
        json.dumps(items),
    )
    return TodoList(id=todo_id, owner=owner, items=items)
