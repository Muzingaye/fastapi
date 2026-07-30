from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EventSchema(BaseModel):
    count: int
    bucket: Optional[date] = ""
    page: Optional[str] = ""
    


class EventCreate(BaseModel):
    page: str
    sessionId : str
    description: Optional[str] = ""
    ipAddress :Optional[str] = Field(default="")
    userAgent : Optional[str] = Field(default="")
    referrer : Optional[str]= Field(default="")
    # duration: Optional[int] = Field(default=0)

class EventUpdate(BaseModel):
    page: Optional[str] = ""
    description: Optional[str] = ""