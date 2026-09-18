from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.config import settings

ph = PasswordHasher()

def hash_password(password):
    return ph.hash(password)

def verify_password(password, hashed):
    try:
        return ph.verify(hashed, password)
    except VerifyMismatchError:
        return False

def create_token(data, token_type, expires):
    payload = data.copy()
    payload["type"] = token_type
    payload["exp"] = datetime.now(timezone.utc) + expires
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(user_id, role):
    return create_token({"sub": str(user_id), "role": role}, "access", timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(user_id):
    return create_token({"sub": str(user_id)}, "refresh", timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

def decode_token(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
