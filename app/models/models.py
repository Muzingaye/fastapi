from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from .database import Base


class Post(Base):
    __tablename__ = 'Posts'
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    createdDate = Column(
        DateTime,
        nullable=False,
        server_default=func.now()   # or text("GETDATE()")
    )
    