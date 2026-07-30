import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import os
from collections.abc import AsyncGenerator


os.environ["DATABASE_URL"] = (f"mssql+pyodbc://localhost/FastApiTestDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&timezone=UTC")
os.environ["BUCKET_NAME"] = "test"
os.environ["SECRET-KEY"] = "test_secret-key-for-testing-only"


os.environ["ACCESS-KEY_ID"] = "testing"
os.environ["SECRET-ACCESS-KEY"] = "testing"
os.environ["REGION"] = "test_secret-key-for-testing-only"

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from api.models.database import Base, get_db
from api.app import app


pytest_plugin = ["anyio"]

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"



@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        poolclass= NullPool,
    )
    return engine


@pytest.fixture(scope="session")
async def setup_database(test_engin):
    async with test_engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    async with test_engin.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()



@pytest.fixture
async def db_session(
    test_engine, setup_database
) -> AsyncGenerator[AsyncSession]:
    conn = await test_engine.connect()
    trans = await conn.begin()

    test_async_session = async_sessionmaker(
        bind=conn,
        class_ = AsyncSession,
        expire_on_commit=False,
        join_transaction_mode = "create_savepoint",
    )


    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()


@pytest.fixture
async def create_user(
    client: AsyncClient,
    email: str = "test@example.com",
    password: str = "password123",
)-> str:
    resp = await client.post("/users",
                            json = {
                                  "email": email,
                                  "password": password,    
                            },
                        )
    assert resp.status_code == 201, f"Failed to create the user, {resp.text}"
    return resp.json()


@pytest.fixture
async def login(
    client: AsyncClient,
    email: str = "test@example.com",
    password: str = "password123",
)-> str:
    resp = await client.post("/auth",
                            data = {
                            "email": email,
                            "password": password,
                        },
                    )
    assert resp.status_code == 200, f"Failed to login {resp.text}"
    return resp.json()["access_token"]

def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}



@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(base_url="http://127.0.0.1:8000") as acc:
        yield acc
