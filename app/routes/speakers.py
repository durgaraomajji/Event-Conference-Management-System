from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.speaker import Speaker
from app.schemas.common import SpeakerCreate
from app.dependencies import require_roles
router=APIRouter(prefix="/speakers",tags=["Speakers"])
@router.post("")
def create(data:SpeakerCreate,db:Session=Depends(get_db),user=Depends(require_roles("Admin","Event Organizer"))):
    if db.query(Speaker).filter(Speaker.email==data.email).first():raise HTTPException(400,"Speaker already exists")
    x=Speaker(**data.model_dump());db.add(x);db.commit();db.refresh(x);return x
@router.get("")
def list_all(db:Session=Depends(get_db)):return db.query(Speaker).all()
@router.get("/{speaker_id}")
def get(speaker_id:int,db:Session=Depends(get_db)):
    x=db.query(Speaker).filter(Speaker.id==speaker_id).first()
    if not x:raise HTTPException(404,"Speaker not found")
    return x
@router.put("/{speaker_id}")
def update(speaker_id:int,data:SpeakerCreate,db:Session=Depends(get_db),user=Depends(require_roles("Admin","Event Organizer"))):
    x=db.query(Speaker).filter(Speaker.id==speaker_id).first()
    if not x:raise HTTPException(404,"Speaker not found")
    for k,v in data.model_dump().items():setattr(x,k,v)
    db.commit();db.refresh(x);return x
