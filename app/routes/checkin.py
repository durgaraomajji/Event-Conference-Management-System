from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.registration import Registration
from app.models.checkin import CheckIn
from app.dependencies import get_current_user,require_roles
router=APIRouter(tags=["Check-In"])
@router.post("/registrations/{registration_id}/check-in")
def checkin(registration_id:int,method:str="Manual",db:Session=Depends(get_db),user=Depends(require_roles("Admin","Staff"))):
    r=db.query(Registration).filter(Registration.id==registration_id).first()
    if not r or r.registration_status!="Confirmed":raise HTTPException(400,"Only confirmed registrations can check in")
    if db.query(CheckIn).filter(CheckIn.registration_id==registration_id).first():raise HTTPException(400,"Duplicate check-in")
    x=CheckIn(registration_id=registration_id,check_in_time=datetime.now(timezone.utc).replace(tzinfo=None),check_in_method=method)
    r.registration_status="Attended";db.add(x);db.commit();db.refresh(x);return x
@router.post("/registrations/{registration_id}/check-out")
def checkout(registration_id:int,db:Session=Depends(get_db),user=Depends(require_roles("Admin","Staff"))):
    x=db.query(CheckIn).filter(CheckIn.registration_id==registration_id).first()
    if not x:raise HTTPException(404,"Check-in not found")
    if x.check_out_time:raise HTTPException(400,"Already checked out")
    x.check_out_time=datetime.now(timezone.utc).replace(tzinfo=None);db.commit();return x
@router.get("/events/{event_id}/attendance")
def attendance(event_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    return db.query(CheckIn).join(Registration,CheckIn.registration_id==Registration.id).filter(Registration.event_id==event_id).all()
