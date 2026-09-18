from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.purchase import Purchase
from app.models.payment import Payment
from app.models.registration import Registration
from app.schemas.common import PaymentCreate
from app.dependencies import get_current_user
router=APIRouter(tags=["Payments"])
@router.post("/payments/{purchase_id}")
def pay(purchase_id:int,data:PaymentCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    p=db.query(Purchase).filter(Purchase.id==purchase_id).first()
    if not p:raise HTTPException(404,"Purchase not found")
    if db.query(Payment).filter(Payment.transaction_id==data.transaction_id).first():raise HTTPException(400,"Duplicate transaction")
    if float(data.amount)!=float(p.total_amount):raise HTTPException(400,"Payment amount must match purchase amount")
    status=data.payment_status
    if status not in ("Success","Failed","Pending"):raise HTTPException(400,"Invalid payment status")
    payment=Payment(purchase_id=p.id,transaction_id=data.transaction_id,payment_method=data.payment_method,amount=data.amount,payment_status=status,payment_date=datetime.now(timezone.utc).replace(tzinfo=None))
    db.add(payment)
    if status=="Success":
        p.purchase_status="Paid"
        r=db.query(Registration).filter(Registration.id==p.registration_id).first()
        r.registration_status="Confirmed"
    db.commit();db.refresh(payment);return payment
@router.get("/payments/{payment_id}")
def get(payment_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    x=db.query(Payment).filter(Payment.id==payment_id).first()
    if not x:raise HTTPException(404,"Payment not found")
    return x
