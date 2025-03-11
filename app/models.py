from pydantic import BaseModel
from typing import List


class CreateTodoList(BaseModel):
    owner: str
    items: List[str] = []


class EditTodoList(BaseModel):
    owner: str
    items: List[str]


class TodoList(BaseModel):
    id: int
    owner: str
    items: List[str]
