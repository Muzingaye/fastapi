from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..db.database import Base


class Vote(Base):
    __tablename__ = "Votes"
    __table_args__ = {"schema": "dbo"}

    userId = Column(Integer, ForeignKey("dbo.Users.id", ondelete="Cascade"), primary_key= True)
    postId = Column(Integer, ForeignKey("dbo.Posts.id", ondelete="Cascade"), primary_key= False)