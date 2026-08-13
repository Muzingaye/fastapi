from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..db.database import Base

# from .post import Post


class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    id : Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[int] = Column(String(320), nullable=False, unique=True)
    password: Mapped[int] = Column(String(255), nullable=False)
    createdDate: Mapped[DateTime] = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="owner"
    )


# class RevokedToken(Base):
#     __tablename__ = "revoked_tokens"

#     id = Column(Integer, primary_key=True, index=True)
#     token = Column(String, unique=True, nullable=False)