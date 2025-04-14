from passlib.hash import pbkdf2_sha256
import jwt, asyncio
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, Request, Depends
from functools import wraps
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from sqlalchemy.orm import Session
from database.db import get_db
from models import users


def hash_password(password: str):
    return pbkdf2_sha256.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy() 
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token):
    return jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)


def check_authorization(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        headers = request.headers
        try:
            jwt_token = headers['Authorization'].split(" ",1)[1]
            if decode_token(token=jwt_token) is False:
                raise HTTPException(status_code=401, detail="Invalid Token")
            
            if asyncio.iscoroutinefunction(func):
                return await func(request, *args, **kwargs)
            else:
                return func(request, *args, **kwargs)
        except Exception as ex:
            raise HTTPException(status_code=401, detail=str(ex))
    return wrapper
        
        
def get_current_user(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = decode_token(token)
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user_id = int(user_id)
        
        current_user = db.query(users.Users).filter(
            users.Users.user_id == user_id,
            users.Users.is_deleted == False
        ).first()

        if current_user is None:
            raise HTTPException(status_code=404, detail="User not found or deleted")

        return current_user
    except Exception as ex:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {ex}")
