from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base


class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True)
    email = Column(String(320), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    createdDate = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    posts = relationship(
        "Post",
        back_populates="owner"
    )


# class RevokedToken(Base):
#     __tablename__ = "revoked_tokens"

#     id = Column(Integer, primary_key=True, index=True)
#     token = Column(String, unique=True, nullable=False)