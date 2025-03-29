from sqlalchemy.orm import Session
from . import models
from schemas import users as schemas
from models.users.hash import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()
    
    
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.user_id == user_id).first()
    

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.Users(
        email = user.email,
        name = user.name,
        hashed_password = hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    print(user)
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return True
    

