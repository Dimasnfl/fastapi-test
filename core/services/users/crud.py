from sqlalchemy.orm import Session
from models import users
from schemas import users as schemas
from core.security import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(users.Users).filter(users.Users.email == email).first()
    
    
def get_user_by_id(db: Session, user_id: int):
    return db.query(users.Users).filter(users.Users.user_id == user_id).first()
    

def create_user(db: Session, user: schemas.UserCreate):
    db_user = users.Users(
        email = user.email,
        name = user.name,
        hashed_password = hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

