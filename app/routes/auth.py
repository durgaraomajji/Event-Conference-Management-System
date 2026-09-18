from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.common import UserCreate, LoginRequest, RefreshRequest, UserOut
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(full_name=data.full_name, email=data.email, phone=data.phone, password_hash=hash_password(data.password), role="Attendee", is_active=True)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    if not user.is_active:
        raise HTTPException(403, "Account is inactive")
    return {"access_token": create_access_token(user.id, user.role), "refresh_token": create_refresh_token(user.id), "token_type": "bearer"}

@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user or not user.is_active:
        raise HTTPException(401, "Invalid user")
    return {"access_token": create_access_token(user.id, user.role), "refresh_token": create_refresh_token(user.id), "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
