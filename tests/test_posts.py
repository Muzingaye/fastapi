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
async def test_create_post_success(client: AsyncClient, login):
    token = login
    headers = auth_header(token)

    resp = await client.post(
        "/posts", json={
            "title": "My Post", "content": "This is the context",
        },
        headers=headers,
    )

    print("STATUS:", resp.status_code)
    print("BODY:", resp.text)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My Post"
    assert data["content"] == "This is the context"
    assert data["createdDate"] is not None

@pytest.mark.anyio
async def test_create_post_unsuccess(client: AsyncClient):
    resp = await client.post(
        "/posts", json={
            "title": "My Post", "content": "This is the context",
        }
    )

    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"




@pytest.mark.anyio
async def test_update_post_success(client: AsyncClient, login):
    token = login
    headers = auth_header(token)

    resp = await client.put(
        "/posts/29", json={
            "title": "My Post Update", "content": "This is an update context",
        },
        headers=headers,
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "My Post Update"
    assert data["content"] == "This is an update context"



@pytest.mark.anyio
async def test_update_post_wrong_user(client: AsyncClient, login):
    token = login
    headers = auth_header(token)

    resp = await client.put(
        "/posts/20", json={
            "title": "My Post Update", "content": "This is an update context",
        },
        headers=headers,
    )

    assert resp.status_code == 403
    data = resp.json()
    assert data["detail"] == "Not authorized to update this post"


@pytest.mark.anyio
async def test_get_post_with_pagination(client: AsyncClient):
    resp  = await client.get("/posts")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0


    resp  = await client.get("/posts?limit=7")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 7
