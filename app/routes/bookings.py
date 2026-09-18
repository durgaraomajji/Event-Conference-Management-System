from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session import EventSession
from app.models.registration import Registration
from app.models.session_booking import SessionBooking
from app.dependencies import get_current_user
router=APIRouter(tags=["Session Bookings"])
@router.post("/sessions/{session_id}/book")
def book(session_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    s=db.query(EventSession).filter(EventSession.id==session_id).first()
    if not s:raise HTTPException(404,"Session not found")
    r=db.query(Registration).filter(Registration.attendee_id==user.id,Registration.event_id==s.event_id,Registration.registration_status.in_(["Confirmed","Attended"])).first()
    if not r:raise HTTPException(403,"Only confirmed attendees can book")
    if db.query(SessionBooking).filter(SessionBooking.session_id==session_id,SessionBooking.registration_id==r.id).first():raise HTTPException(400,"Duplicate booking")
    if db.query(SessionBooking).filter(SessionBooking.session_id==session_id).count()>=s.capacity:raise HTTPException(400,"Session capacity exceeded")
    x=SessionBooking(session_id=session_id,registration_id=r.id,booking_date=datetime.now(timezone.utc).replace(tzinfo=None));db.add(x);db.commit();db.refresh(x);return x
@router.get("/attendees/{attendee_id}/sessions")
def attendee_sessions(attendee_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    return db.query(SessionBooking).join(Registration,SessionBooking.registration_id==Registration.id).filter(Registration.attendee_id==attendee_id).all()
@router.delete("/session-bookings/{booking_id}")
def cancel(booking_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    x=db.query(SessionBooking).filter(SessionBooking.id==booking_id).first()
    if not x:raise HTTPException(404,"Booking not found")
    db.delete(x);db.commit();return {"message":"Booking cancelled"}
