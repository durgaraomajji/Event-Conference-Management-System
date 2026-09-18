from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.feedback import Feedback
from app.models.checkin import CheckIn
from app.schemas.common import FeedbackCreate
from app.dependencies import get_current_user
router=APIRouter(tags=["Feedback"])
@router.post("/feedback")
def create(data:FeedbackCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    r=db.query(CheckIn).filter(CheckIn.registration_id==data.registration_id).first()
    if not r:raise HTTPException(403,"Only attendees who checked in can provide feedback")
    if data.session_id and db.query(Feedback).filter(Feedback.registration_id==data.registration_id,Feedback.session_id==data.session_id).first():raise HTTPException(400,"Duplicate feedback")
    x=Feedback(**data.model_dump());db.add(x);db.commit();db.refresh(x);return x
@router.get("/events/{event_id}/feedback")
def event_feedback(event_id:int,db:Session=Depends(get_db)):return db.query(Feedback).filter(Feedback.event_id==event_id).all()
@router.get("/speakers/{speaker_id}/ratings")
def speaker_ratings(speaker_id:int,db:Session=Depends(get_db)):return db.query(Feedback).filter(Feedback.speaker_id==speaker_id).all()
