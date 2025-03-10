from pydantic import BaseModel


class CreateTodoList(BaseModel):
    owner: str
    items: list[str] = []


class EditTodoList(BaseModel):
    owner: str
    items: list[str]


class TodoList(BaseModel):
    id: int
    owner: str
    items: list[str]
