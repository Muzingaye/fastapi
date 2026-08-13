from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (DeclarativeBase, declarative_base, relationship,
                            sessionmaker)

from api.config import settings
from fastapi import Request

SQL_DATABASE_URL = (
    f"mssql+pyodbc://{settings.database_hostname}/"
    f"{settings.database_name}"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&timezone=UTC"
)
# create_engine(SQL_DATABASE_URL, timezone="UTC")
engine= create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,  bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Cater for graphql context
def get_graphql_context(request: Request):

    db = SessionLocal()

    return {
        "request": request,
        "db": db
    }