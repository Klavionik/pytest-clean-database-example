from fastapi import APIRouter, Depends
from app.models import User, CreateUser, TodoList, CreateTodoList, EditTodoList
from app.deps import get_database
from asyncpg import Connection
import json

router = APIRouter(prefix="/api/v1")


@router.get("/users")
async def list_users(database: Connection = Depends(get_database)) -> list[User]:
    rows = await database.fetch("SELECT * FROM users;")
    return [User(**row) for row in rows]


@router.post("/users", status_code=201)
async def create_user(user: CreateUser, database: Connection = Depends(get_database)) -> User:
    row = await database.fetchrow("INSERT INTO users (username) VALUES ($1) RETURNING id;", user.username)
    return User(id=row["id"], username=user.username)


@router.get("/todos")
async def list_todos(database: Connection = Depends(get_database)) -> list[TodoList]:
    rows = await database.fetch("SELECT todos.id, username, user_id, items FROM todos JOIN users ON todos.user_id = users.id;")
    return [TodoList(id=row["id"], user=User(username=row["username"], id=row["user_id"]), items=json.loads(row["items"])) for row in rows]


@router.post("/todos", status_code=201)
async def create_todo(todo: CreateTodoList, database: Connection = Depends(get_database)) -> TodoList:
    row = await database.fetchrow("INSERT INTO todos (user_id, items) VALUES ($1, $2) RETURNING id;", todo.user_id, json.dumps(todo.items))
    user_row = await database.fetchrow("SELECT username FROM users WHERE id = $1;", todo.user_id)
    return TodoList(id=row["id"], user=User(id=todo.user_id, username=user_row["username"]), items=todo.items)


@router.put("/todos/{todo_id}")
async def edit_todo(todo_id: int, todo: EditTodoList, database: Connection = Depends(get_database)) -> TodoList:
    await database.fetchrow("UPDATE todos SET items = $2 WHERE id = $1", todo_id, json.dumps(todo.items))
    user_row = await database.fetchrow("SELECT users.id, username FROM users JOIN todos ON users.id = todos.user_id WHERE todos.id = $1;", todo_id)
    return TodoList(id=todo_id, user=User(id=user_row["id"], username=user_row["username"]), items=todo.items)
