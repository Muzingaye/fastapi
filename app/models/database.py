from collections.abc import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
from app.config import settings

SQL_DATABASE_URL = (
    f"mssql+pyodbc://{settings.database_hostname}/"
    f"{settings.database_name}"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine= create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,  bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
