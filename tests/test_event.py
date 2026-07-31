import pytest
from httpx import AsyncClient

from tests.conftest import auth_header, login

@pytest.mark.anyio
async def test_get_event(client: AsyncClient):
    resp = await client.get("/event/1",  follow_redirects=True)
    assert len(resp.json()) == 1


@pytest.mark.anyio
async def test_get_event_not_found(client: AsyncClient):
    resp = await client.get("/event/99999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Not Found"



@pytest.mark.anyio
async def test_create_user_duplicate_email(
    client: AsyncClient,
    # create_user,
):
    # await create_user(
    #     email="mtester@example.com",
    #     password="password123",
    # )

    response = await client.post(
        "/user",
        json={
            "email": "mtester@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
