from fastapi import APIRouter
from ..schemas import EventSchema,EventCreate, EventUpdate
from typing import List


router = APIRouter(
    prefix="/events",
    tags= ["Events"]
)


@router.get('/{id}', response_model =EventSchema)
def get_event(id: int):
    return {"id": id}


@router.get('/', response_model =List[EventSchema])
def read_event():
    return[
                {"id": 2}, 
                {"id": 3}
            ]


@router.post("/", response_model=EventSchema)
def create_event(payload: EventCreate):
    print(payload)
    return {"id": id,"page": payload.page, "description": payload.description}


@router.put("/{id}", response_model = EventSchema)
def update_event(id: int, payload: EventCreate):
    print(payload)
    return {"id": id,"page": payload.page, "description": payload.description}
