from sqlalchemy import Index, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from api.db.database import Base
import sqlmodel
from sqlmodel import SQLModel
from datetime import datetime, timezone
from timescaledb import TimescaleModel


def get_utc_now():
    return datetime.now(timezone.now).replace(tzinfo=timezone.utc)


class Event(Base):
    __tablename__ = 'Events'
    __table_args__ = {"schema": "dbo"}
    __table_args__ = (
        # Index("ix_pagevisits_createdDate", "createdDate"),
        # Index("ix_pagevisits_page_createdDate", "page", "createdDate"),
        # Index("ix_events_createdDate", "createdDate"),
        # {"schema": "dbo"}
    )

    id = Column(Integer, primary_key=True)
    page = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    userId = Column(Integer, nullable=True)
    sessionId = Column(String(100), nullable=True)
    # duration =  Column(Integer)
    ipAddress = Column(String(50), nullable=True)
    userAgent = Column(String(500), nullable=True)
    referrer = Column(String(500), nullable=True)


    # __chuck_time_interval__ =""
    # __drop_after__ = ""
   
    createdDate = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        # server_default=get_utc_now
        # sa_type= sqlmodel.DateTime(timezone=True)
    )
    # userId = Column(Integer, ForeignKey("dbo.Users.id", ondelete="Cascade"),
    #                  nullable= False)
    # owner = relationship("User",foreign_keys=[userId] )

