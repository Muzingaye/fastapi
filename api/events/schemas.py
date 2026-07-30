from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EventSchema(BaseModel):
    count: int
    bucket: Optional[date] = ""
    page: Optional[str] = ""
    


class EventCreate(BaseModel):
    page: str
    description: Optional[str] = Field("my default description")
   


class EventUpdate(BaseModel):
    page: Optional[str] = ""
    description: Optional[str] = ""