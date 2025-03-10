from fastapi import APIRouter, Depends

from app.models import TodoList, CreateTodoList, EditTodoList
from app.deps import get_db_connection
from asyncpg import Connection
from app import crud

router = APIRouter(prefix="/api/v1")


@router.get("/todos")
async def list_todos(conn: Connection = Depends(get_db_connection)) -> list[TodoList]:
    return await crud.list_todos(conn)


@router.post("/todos", status_code=201)
async def create_todo(
    todo: CreateTodoList, conn: Connection = Depends(get_db_connection)
) -> TodoList:
    return await crud.create_todo(todo.owner, todo.items, conn)


@router.put("/todos/{todo_id}")
async def edit_todo(
    todo_id: int, todo: EditTodoList, conn: Connection = Depends(get_db_connection)
) -> TodoList:
    return await crud.edit_todo(todo_id, todo.owner, todo.items, conn)
