from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, cast, Date
from timescaledb.hyperfunctions import time_bucket
from sqlalchemy.orm import Session
from ..schemas import EventSchema,EventCreate, EventUpdate
from typing import List
from ..models import Event
from api.models.database import engine, get_db
from api.models import oauth2


router = APIRouter(
    prefix="/events",
    tags= ["Events"]
)


@router.get('/{id}', response_model =EventSchema)
def get_event(id: int, db:Session = Depends(get_db),limit:int =10):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'event with id: {id} was not found')

    return event


@router.get('/', response_model =List[EventSchema])
def read_event(db:Session = Depends(get_db),limit:int =10):
    query = (
        select(
            cast(Event.createdDate, Date).label("bucket"),
            Event.page.label('page'),
            func.count().label("count"),
        )
        # .where(
        #     Event.createdDate >= start,
        #     Event.createdDate <= finished
        # )
        .group_by(
            cast(Event.createdDate, Date),
            Event.page,
        )
        .order_by(
            cast(Event.createdDate, Date).desc()
        )
    )
    results = db.execute(query).all()
    # print(results)
    # events = db.query(Event).order_by(Event.createdDate.desc()).limit(10).all()
    if not results:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'No Upcoming ost found')
    return results
        


@router.post("/", response_model=EventSchema)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
                #   ?curr_user: int = Depends(oauth2.get_current_user)):
    new_event = Event(**payload.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.put("/{id}", response_model = EventSchema)
def update_event(id: int, payload: EventCreate, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == id).first()
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event with id: {id} was not found')
    

    for k, v in payload.model_dump().items():
        setattr(db_event, k, v)

    db.commit()
    db.refresh(db_event)
    return db_event
