from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ticket import Ticket
from app.models.registration import Registration
from app.models.purchase import Purchase
from app.schemas.common import PurchaseCreate
from app.dependencies import get_current_user
router=APIRouter(tags=["Purchases"])
@router.post("/tickets/{ticket_id}/purchase")
def purchase(ticket_id:int,data:PurchaseCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    t=db.query(Ticket).filter(Ticket.id==ticket_id).with_for_update().first()
    if not t:raise HTTPException(404,"Ticket not found")
    now=datetime.now(timezone.utc).replace(tzinfo=None)
    if not(t.sale_start<=now<=t.sale_end):raise HTTPException(400,"Ticket sale period expired")
    if data.quantity>t.available_quantity:raise HTTPException(400,"Insufficient ticket quantity")
    r=db.query(Registration).filter(Registration.attendee_id==user.id,Registration.event_id==t.event_id,Registration.registration_status!="Cancelled").first()
    if not r:raise HTTPException(400,"Register for event first")
    subtotal=float(t.price)*data.quantity
    tax=round(subtotal*0.18,2)
    total=subtotal+tax
    t.available_quantity-=data.quantity
    p=Purchase(registration_id=r.id,ticket_id=t.id,quantity=data.quantity,subtotal=subtotal,discount=0,tax=tax,total_amount=total)
    db.add(p);db.commit();db.refresh(p);return p
@router.get("/purchases/{purchase_id}")
def get(purchase_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    p=db.query(Purchase).filter(Purchase.id==purchase_id).first()
    if not p:raise HTTPException(404,"Purchase not found")
    return p
