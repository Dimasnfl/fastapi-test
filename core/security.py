from passlib.hash import pbkdf2_sha256
import jwt, asyncio
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from functools import wraps
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


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
        