from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = 'Posts'
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    # url = Column(String, nullable=False)
    # fileType = Column(String, nullable= False)
    # fileName = Column(String(nullable=False))
    published = Column(Boolean, server_default='True', nullable=False)
    createdDate = Column(
        DateTime,
        nullable=False,
        server_default=func.now()   # or text("GETDATE()")
    )
    userId = Column(Integer, ForeignKey("dbo.Users.id", ondelete="Cascade"),
                     nullable= False)
    owner = relationship("User",foreign_keys=[userId] )



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



class Vote(Base):
    __tablename__ = "Votes"
    __table_args__ = {"schema": "dbo"}

    userId = Column(Integer, ForeignKey("dbo.Users.id", ondelete="Cascade"), primary_key= True)
    postId = Column(Integer, ForeignKey("dbo.Posts.id", ondelete="Cascade"), primary_key= False)