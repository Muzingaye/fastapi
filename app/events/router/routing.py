from fastapi import APIRouter
from .. schemas import EventSchema


router = APIRouter(
    prefix="/events",
    tags= ["Events"]
)


@router.get('/{id}', response_model =EventSchema)
def get_event(id: int):
    return {"id": id}


@router.get("/")
def read_event():
    return {
    "results": [1,2,3]}