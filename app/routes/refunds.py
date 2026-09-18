from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.purchase import Purchase
from app.models.refund import Refund
from app.models.event import Event
from app.models.registration import Registration
from app.dependencies import get_current_user
router=APIRouter(prefix="/refunds",tags=["Refunds"])
@router.post("/purchases/{purchase_id}")
def refund(purchase_id:int,reason:str,db:Session=Depends(get_db),user=Depends(get_current_user)):
    p=db.query(Purchase).filter(Purchase.id==purchase_id).first()
    if not p:raise HTTPException(404,"Purchase not found")
    r=db.query(Registration).filter(Registration.id==p.registration_id).first()
    e=db.query(Event).filter(Event.id==r.event_id).first()
    amount=float(p.total_amount)
    if e and e.status!="Cancelled" and e.start_date>datetime.now():
        days=(e.start_date-datetime.now()).days
        amount=amount if days>=7 else amount*0.5
    x=Refund(purchase_id=p.id,cancellation_reason=reason,refund_amount=amount,refund_status="Processed",refund_date=datetime.now(timezone.utc).replace(tzinfo=None))
    db.add(x);db.commit();db.refresh(x);return x
