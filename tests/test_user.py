from io import BytesIO
from pathlib import Path
from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient

from tests.conftest import auth_header, create_user, login




@pytest.mark.anyio
async def test_create_user_validation_errors(client: AsyncClient):
    resp = await client.post(
            "/user", json={
                "email": "Something junk",
            },
        )
    assert resp.status_code == 422
    assert "email" in resp.text
    assert "password" in resp.text


@pytest.mark.anyio
async def test_create_user_duplicate_email(client: AsyncClient, create_user):
    await create_user

    response = await client.post(
        "/user",
        json={
            "email": "mtester@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    print(response.json()["detail"])
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.anyio
async def test_create_user_success(client: AsyncClient):
    response = await client.post(
        "/user",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert data["createdDate"] is not None


# @pytest.mark.anyio
# async def test_forgot_password_sends_email(client: AsyncClient, create_user):
#     user = create_user

#     with patch(
#         "routers.users.send_password_reset_email",
#         new_callable=AsyncMock,
#     ) as mock_send:
#         response = await client.post(
#             "/api/users/forgot-password",
#             json={"email": "test@example.com"},
#         )

#         assert response.status_code == 202
#         mock_send.assert_awaited_once()
#         call_kwargs = mock_send.call_args.kwargs
#         assert call_kwargs["to_email"] == "test@example.com"
#         assert "token" in call_kwargs
