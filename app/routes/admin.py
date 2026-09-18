from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies import require_roles
router=APIRouter(prefix="/admin",tags=["Admin"])
@router.post("/users/{user_id}/activate")
def activate(user_id:int,db:Session=Depends(get_db),user=Depends(require_roles("Admin"))):
    x=db.query(User).filter(User.id==user_id).first()
    if not x:raise HTTPException(404,"User not found")
    x.is_active=True;db.commit();return {"message":"Account activated"}
@router.post("/users/{user_id}/deactivate")
def deactivate(user_id:int,db:Session=Depends(get_db),user=Depends(require_roles("Admin"))):
    x=db.query(User).filter(User.id==user_id).first()
    if not x:raise HTTPException(404,"User not found")
    x.is_active=False;db.commit();return {"message":"Account deactivated"}
