from pydantic import BaseModel, Field
from typing import Optional

class EventSchema(BaseModel):
    id: int
    page: Optional[str] = ""
    description: Optional[str] = ""
    


class EventCreate(BaseModel):
    page: str
    description: Optional[str] = Field("my default description")
   


class EventUpdate(BaseModel):
    page: Optional[str] = ""
    description: Optional[str] = ""