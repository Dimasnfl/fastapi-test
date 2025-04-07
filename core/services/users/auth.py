from sqlalchemy.orm import Session
from core.services.users import crud
from core.security import verify_password


def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    print(user)
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return True