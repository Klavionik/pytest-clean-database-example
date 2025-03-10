from asyncpg import Connection
from httpx import AsyncClient
from app import crud


async def test_create_todo(test_client: AsyncClient) -> None:
    response = await test_client.post("/api/v1/todos", json={"owner": "jediroman"})

    assert response.status_code == 201
    assert response.json()["owner"] == "jediroman"


async def test_edit_todo(test_client: AsyncClient, test_connection: Connection) -> None:
    todo = await crud.create_todo(owner="jediroman", items=[], conn=test_connection)

    response = await test_client.put(
        f"/api/v1/todos/{todo.id}",
        json={"owner": "jediroman", "items": ["go to sleep"]},
    )
    edited_todo = response.json()

    assert response.status_code == 200
    assert edited_todo["items"] == ["go to sleep"]


async def test_list_todos_no_todos(test_client: AsyncClient) -> None:
    response = await test_client.get("/api/v1/todos")
    todos_list = response.json()

    assert response.status_code == 200
    assert not len(todos_list)


async def test_list_todos(
    test_client: AsyncClient, test_connection: Connection
) -> None:
    await crud.create_todo(
        owner="jediroman", items=["fool around"], conn=test_connection
    )
    await crud.create_todo(owner="jesuisgmo", items=["study"], conn=test_connection)

    response = await test_client.get("/api/v1/todos")
    todos_list = response.json()

    assert response.status_code == 200
    assert len(todos_list) == 2
