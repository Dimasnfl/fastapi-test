from fastapi import APIRouter, Depends, HTTPException, UploadFile, responses, Request
from sqlalchemy.orm import Session
from core import security
from core.services.users import auth
from database.db import get_db
from models import users as Models
from schemas import users as Schemas
from datetime import timedelta
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.services.users import crud


router = APIRouter(
    tags=["users"],
    responses={404: {"message": "User not found"}}
)

@router.post("/auth/login")
async def login_user(user: Schemas.LoginUser, db: Session = Depends(get_db)):
    if auth.authenticate_user(db, user.email, user.password) is False:
        return responses.JSONResponse(content={
            "message": "Invalid credentials"
        }, status_code=401)
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data= {
            "sub": user.email
        },
        expires_delta = access_token_expires
    )
    
    return responses.JSONResponse(content={
        "message": "Login successfull",
        "access_token": access_token,
        "token_type": "bearer"
    }, status_code=200)
    
    

@router.get("/", response_model=Schemas.GetUsersResponse)
@security.check_authorization
async def get_all_user(request: Request, db: Session = Depends(get_db)):
    data = crud.get_active_users(db)
    users_response = [Schemas.GetUsers.model_validate(user) for user in data]
    return {
        "message": "List of active users",
        "data": users_response
    }
    


@router.get("/{user_id}", response_model=Schemas.GetUsers)
@security.check_authorization
async def get_user_by_id(request: Request, user_id: int, db: Session = Depends(get_db)):
    data = crud.get_user_by_id(db, user_id=user_id)
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return data



@router.post("/create-user", response_model=Schemas.GetCreateUsersResponse)
async def create_user(request: Request, user: Schemas.CreateUser, db: Session = Depends(get_db)):
    get_email = crud.get_user_by_email(db, email=user.email)
    if get_email:
        raise HTTPException(status_code=400, detail="Email already registered with another user")
    
    data = crud.create_user(db=db, user=user)
    users_response = Schemas.GetCreatedUser.model_validate(data)

    return {
        "message": "User created successfully",
        "data": users_response
    }



@router.delete("/{user_id}")
@security.check_authorization
async def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    data = crud.soft_delete_user(db, user_id=user_id)
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}



@router.post("/upload-img")
@security.check_authorization
async def upload_img(request: Request, uploaded_file: UploadFile):
    file_location = f"static/img/{uploaded_file.filename}"
    contents = await uploaded_file.read()
    
    with open(file_location, "wb+") as file_object:
        file_object.write(contents)
        
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}