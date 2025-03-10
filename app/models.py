from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str


class User(CreateUser):
    id: int


class CreateTodoList(BaseModel):
    user_id: int
    items: list[str] = []


class EditTodoList(BaseModel):
    items: list[str]


class TodoList(BaseModel):
    id: int
    user: User
    items: list[str]
