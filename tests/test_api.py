from httpx import AsyncClient


async def test_create_user(test_client: AsyncClient) -> None:
    response = await test_client.post("/api/v1/users", json={"username": "jediroman"})

    assert response.status_code == 201
    assert response.json()["username"] == "jediroman"


async def test_create_todo(test_client: AsyncClient) -> None:
    user_response = await test_client.post("/api/v1/users", json={"username": "jediroman"})
    user = user_response.json()

    response = await test_client.post("/api/v1/todos", json={"user_id": user["id"]})
    todo = response.json()

    assert response.status_code == 201
    assert todo["items"] == []
    assert todo["user"] == {"id": user["id"], "username": user["username"]}