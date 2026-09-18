from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event import Event
from app.models.session import EventSession
from app.schemas.session import SessionCreate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])


def normalize_datetime(value):
    if value is not None and value.tzinfo is not None:
        return value.replace(tzinfo=None)
    return value


def validate(data, db):
    event = db.query(Event).filter(Event.id == data.event_id).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    start_time = normalize_datetime(data.start_time)
    end_time = normalize_datetime(data.end_time)
    event_start = normalize_datetime(event.start_date)
    event_end = normalize_datetime(event.end_date)

    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="Session end time must be after start time"
        )

    if start_time < event_start or end_time > event_end:
        raise HTTPException(
            status_code=400,
            detail="Session timing must be within event timing"
        )


@router.post("/", response_model=SessionResponse)
def create(
    data: SessionCreate,
    db: Session = Depends(get_db)
):
    validate(data, db)

    session_data = data.model_dump()
    session_data["start_time"] = normalize_datetime(
        session_data["start_time"]
    )
    session_data["end_time"] = normalize_datetime(
        session_data["end_time"]
    )

    session = EventSession(**session_data)

    db.add(session)
    db.commit()
    db.refresh(session)

    return session