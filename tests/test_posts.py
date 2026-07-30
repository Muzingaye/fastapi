import pytest
from httpx import AsyncClient

from tests.conftest import auth_header, create_user, login

@pytest.mark.anyio

async def test_posts_not_found(client: AsyncClient):
    resp = await client.get("/posts/999",  follow_redirects=True)
    assert resp.status_code == 404
    data = resp.json()
    assert data == {
        "detail": "post with id: 999 was not found"
    }


@pytest.mark.anyio
async def test_create_post_success(client: AsyncClient, create_user):
    token = await login(client)
    headers = auth_header(token)

    resp = await client.post(
        "/posts", json={
            "title": "My Post", "content": "This is the context",
        },
        headers=headers,
    )

    assert resp.status_code == 201
    data = resp.json()

    assert data["title"] == "My Post"
    assert data["content"] == "This is the context"
    assert data["userId"] == create_user["id"]
    assert "dateCreated" in data