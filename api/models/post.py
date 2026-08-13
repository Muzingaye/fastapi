from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        func, text)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..db.database import Base


class Post(Base):
    __tablename__ = 'Posts'
    __table_args__ = {"schema": "dbo"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, server_default='True', nullable=False)
    createdDate: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()   # or text("GETDATE()")
    )
    userId : Mapped[int] = mapped_column(Integer, ForeignKey("dbo.Users.id", ondelete="Cascade"),
                     nullable= False)
    owner: Mapped["User"]  = relationship("User",foreign_keys=[userId] )

