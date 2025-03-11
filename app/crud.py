from __future__ import annotations
import json

from mysql.connector.aio import MySQLConnectionAbstract as Connection

from app.models import TodoList


async def list_todos(conn: Connection) -> list[TodoList]:
    async with await conn.cursor() as cur:
        await cur.execute("SELECT id, owner, items FROM todos;")
        rows = await cur.fetchall()

    return [
        TodoList(id=id_, owner=owner, items=json.loads(items))  # type: ignore[arg-type]
        for (id_, owner, items) in rows
    ]


async def create_todo(owner: str, items: list[str], conn: Connection) -> TodoList:
    async with await conn.cursor() as cur:
        await cur.execute(
            "INSERT INTO todos (owner, items) VALUES (%s, %s);",
            (owner, json.dumps(items)),
        )
        assert cur.lastrowid is not None
    return TodoList(id=cur.lastrowid, owner=owner, items=items)


async def edit_todo(
    todo_id: int, owner: str, items: list[str], conn: Connection
) -> TodoList:
    async with await conn.cursor() as cur:
        await cur.execute(
            "UPDATE todos SET owner = %s, items = %s WHERE id = %s;",
            (owner, json.dumps(items), todo_id),
        )
    return TodoList(id=todo_id, owner=owner, items=items)
