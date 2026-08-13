from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..db.database import Base


class Vote(Base):
    __tablename__ = "Votes"
    __table_args__ = {"schema": "dbo"}

    userId = Column(Integer, ForeignKey("dbo.Users.id", ondelete="Cascade"), primary_key= True)
    postId = Column(Integer, ForeignKey("dbo.Posts.id", ondelete="Cascade"), primary_key= False)