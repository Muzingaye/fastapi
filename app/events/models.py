from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base



class Event(Base):
    __tablename__ = 'Events'
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True)
    page = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    # fileName = Column(String(nullable=False))
    # published = Column(Boolean, server_default='True', nullable=False)
    createdDate = Column(
        DateTime,
        nullable=False,
        server_default=func.now()   # or text("GETDATE()")
    )
    # userId = Column(Integer, ForeignKey("dbo.Users.id", ondelete="Cascade"),
    #                  nullable= False)
    # owner = relationship("User",foreign_keys=[userId] )

