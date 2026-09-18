from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.event import Event
from app.models.ticket import Ticket
from app.schemas.common import TicketCreate
from app.dependencies import require_roles
router=APIRouter(prefix="/events/{event_id}/tickets",tags=["Tickets"])
@router.post("")
def create(event_id:int,data:TicketCreate,db:Session=Depends(get_db),user=Depends(require_roles("Admin","Event Organizer"))):
    if not db.query(Event).filter(Event.id==event_id).first():raise HTTPException(404,"Event not found")
    x=Ticket(**data.model_dump(),event_id=event_id,available_quantity=data.quantity);db.add(x);db.commit();db.refresh(x);return x
@router.get("")
def list_all(event_id:int,db:Session=Depends(get_db)):return db.query(Ticket).filter(Ticket.event_id==event_id).all()
