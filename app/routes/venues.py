from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.venue import Venue,Hall
from app.schemas.common import VenueCreate,HallCreate
from app.dependencies import require_roles
router=APIRouter(prefix="/venues",tags=["Venues"])
@router.post("")
def create(data:VenueCreate,db:Session=Depends(get_db),user=Depends(require_roles("Admin","Event Organizer"))):
    x=Venue(**data.model_dump());db.add(x);db.commit();db.refresh(x);return x
@router.get("")
def list_all(db:Session=Depends(get_db)):return db.query(Venue).all()
@router.post("/{venue_id}/halls")
def hall(venue_id:int,data:HallCreate,db:Session=Depends(get_db),user=Depends(require_roles("Admin","Event Organizer"))):
    v=db.query(Venue).filter(Venue.id==venue_id).first()
    if not v:raise HTTPException(404,"Venue not found")
    if data.capacity>v.capacity:raise HTTPException(400,"Hall capacity cannot exceed venue capacity")
    h=Hall(**data.model_dump(),venue_id=venue_id);db.add(h);db.commit();db.refresh(h);return h
@router.get("/{venue_id}/halls")
def halls(venue_id:int,db:Session=Depends(get_db)):return db.query(Hall).filter(Hall.venue_id==venue_id).all()
