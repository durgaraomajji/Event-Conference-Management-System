from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.event import Event
from app.models.registration import Registration
from app.dependencies import get_current_user
router=APIRouter(tags=["Registrations"])
@router.post("/events/{event_id}/register")
def register(event_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    if user.role!="Attendee":raise HTTPException(403,"Only attendees can register")
    e=db.query(Event).filter(Event.id==event_id,Event.is_deleted==False).first()
    if not e:raise HTTPException(404,"Event not found")
    now=datetime.now(timezone.utc).replace(tzinfo=None)
    if e.status=="Cancelled":raise HTTPException(400,"Cancelled events cannot accept registrations")
    if not(e.registration_start<=now<=e.registration_end):raise HTTPException(400,"Registration period is closed")
    if db.query(Registration).filter(Registration.attendee_id==user.id,Registration.event_id==event_id).first():raise HTTPException(400,"Duplicate registration")
    count=db.query(func.count(Registration.id)).filter(Registration.event_id==event_id,Registration.registration_status!="Cancelled").scalar()
    if count>=e.capacity:raise HTTPException(400,"Event capacity exceeded")
    r=Registration(attendee_id=user.id,event_id=event_id,registration_date=now,registration_status="Pending")
    db.add(r);db.commit();db.refresh(r);return r
@router.get("/registrations")
def registrations(event_id:int|None=None,status:str|None=None,db:Session=Depends(get_db),user=Depends(get_current_user)):
    q=db.query(Registration)
    if user.role=="Attendee":q=q.filter(Registration.attendee_id==user.id)
    if event_id:q=q.filter(Registration.event_id==event_id)
    if status:q=q.filter(Registration.registration_status==status)
    return q.all()
@router.get("/registrations/{registration_id}")
def get(registration_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    r=db.query(Registration).filter(Registration.id==registration_id).first()
    if not r:raise HTTPException(404,"Registration not found")
    if user.role=="Attendee" and r.attendee_id!=user.id:raise HTTPException(403,"Not allowed")
    return r
@router.post("/registrations/{registration_id}/cancel")
def cancel(registration_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    r=db.query(Registration).filter(Registration.id==registration_id).first()
    if not r:raise HTTPException(404,"Registration not found")
    if user.role=="Attendee" and r.attendee_id!=user.id:raise HTTPException(403,"Not allowed")
    r.registration_status="Cancelled";db.commit();return r
