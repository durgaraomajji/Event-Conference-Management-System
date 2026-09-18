from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration
from app.models.purchase import Purchase
from app.models.payment import Payment
from app.models.feedback import Feedback
from app.dependencies import require_roles
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])
@router.get("/admin")
def admin(db:Session=Depends(get_db),user=Depends(require_roles("Admin"))):
    revenue=db.query(func.coalesce(func.sum(Payment.amount),0)).filter(Payment.payment_status=="Success").scalar()
    sold=db.query(func.coalesce(func.sum(Purchase.quantity),0)).filter(Purchase.purchase_status=="Paid").scalar()
    rating=db.query(func.coalesce(func.avg(Feedback.rating),0)).scalar()
    return {"total_events":db.query(Event).filter(Event.is_deleted==False).count(),"active_events":db.query(Event).filter(Event.status.in_(["Published","Registration Open"])).count(),"completed_events":db.query(Event).filter(Event.status=="Completed").count(),"total_attendees":db.query(User).filter(User.role=="Attendee").count(),"total_registrations":db.query(Registration).count(),"total_tickets_sold":sold,"total_revenue":float(revenue or 0),"total_refunds":0,"average_event_rating":float(rating or 0)}
