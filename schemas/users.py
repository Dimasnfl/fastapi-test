from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    name: str
    password: str
    
class User(UserBase):
    user_id: int
    name: str

class Config:
    orm_mode = True

class UserLogin(UserBase):
    password: str