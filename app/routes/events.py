from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.event import Event
from app.models.registration import Registration
from app.schemas.common import EventCreate
from app.dependencies import get_current_user, require_roles

router=APIRouter(prefix="/events", tags=["Events"])

def validate_event(data):
    if data.end_date <= data.start_date: raise HTTPException(400,"End date must be after start date")
    if data.registration_end > data.start_date: raise HTTPException(400,"Registration closing date cannot be after event start")
    if data.registration_start >= data.registration_end: raise HTTPException(400,"Invalid registration period")

@router.post("")
def create(data: EventCreate, db:Session=Depends(get_db), user=Depends(require_roles("Admin","Event Organizer"))):
    validate_event(data)
    e=Event(**data.model_dump(), organizer_id=user.id); db.add(e); db.commit(); db.refresh(e); return e

@router.get("")
def list_events(event_type:str|None=None, city:str|None=None, status:str|None=None, page:int=Query(1,ge=1), limit:int=Query(10,ge=1,le=100), db:Session=Depends(get_db)):
    q=db.query(Event).filter(Event.is_deleted==False)
    if event_type:q=q.filter(Event.event_type==event_type)
    if city:q=q.filter(Event.city==city)
    if status:q=q.filter(Event.status==status)
    return q.offset((page-1)*limit).limit(limit).all()

@router.get("/{event_id}")
def get_event(event_id:int,db:Session=Depends(get_db)):
    e=db.query(Event).filter(Event.id==event_id,Event.is_deleted==False).first()
    if not e:raise HTTPException(404,"Event not found")
    return e

@router.put("/{event_id}")
def update(event_id:int,data:EventCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    validate_event(data); e=db.query(Event).filter(Event.id==event_id,Event.is_deleted==False).first()
    if not e:raise HTTPException(404,"Event not found")
    if user.role!="Admin" and e.organizer_id!=user.id:raise HTTPException(403,"Not allowed")
    for k,v in data.model_dump().items():setattr(e,k,v)
    db.commit();db.refresh(e);return e

@router.delete("/{event_id}")
def delete(event_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    e=db.query(Event).filter(Event.id==event_id).first()
    if not e:raise HTTPException(404,"Event not found")
    if user.role!="Admin" and e.organizer_id!=user.id:raise HTTPException(403,"Not allowed")
    e.is_deleted=True;e.status="Cancelled";db.commit();return {"message":"Event cancelled"}
