from datetime import datetime,timezone
import uuid
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.registration import Registration
from app.models.checkin import CheckIn
from app.models.certificate import Certificate
from app.dependencies import get_current_user
router=APIRouter(tags=["Certificates"])
@router.post("/certificates/generate/{registration_id}")
def generate(registration_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    r=db.query(Registration).filter(Registration.id==registration_id).first()
    if not r:raise HTTPException(404,"Registration not found")
    if not db.query(CheckIn).filter(CheckIn.registration_id==registration_id).first():raise HTTPException(400,"Attendance requirement not satisfied")
    if db.query(Certificate).filter(Certificate.event_id==r.event_id,Certificate.attendee_id==r.attendee_id).first():raise HTTPException(400,"Certificate already generated")
    c=Certificate(certificate_number="CERT-"+uuid.uuid4().hex[:12].upper(),attendee_id=r.attendee_id,event_id=r.event_id,issue_date=datetime.now(timezone.utc).replace(tzinfo=None),certificate_type="Participation",status="Issued")
    db.add(c);db.commit();db.refresh(c);return c
@router.get("/certificates/{certificate_id}")
def get(certificate_id:int,db:Session=Depends(get_db)):return db.query(Certificate).filter(Certificate.id==certificate_id).first()
@router.get("/attendees/{attendee_id}/certificates")
def list_certs(attendee_id:int,db:Session=Depends(get_db)):return db.query(Certificate).filter(Certificate.attendee_id==attendee_id).all()
