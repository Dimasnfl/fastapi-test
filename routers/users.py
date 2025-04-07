from fastapi import APIRouter, Depends, HTTPException, UploadFile, responses, Request
from sqlalchemy.orm import Session
from database import get_db
from models.users import crud, models, hash
from schemas import users as Schemas
from datetime import timedelta

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"message": "User not found"}}
)

@router.get("/")
@hash.check_authorization
async def get_all_user(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


@router.get("/{user_id}")
@hash.check_authorization
async def get_user_by_id(request: Request, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/create-user")
@hash.check_authorization
async def create_user(request: Request, user: Schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered with another user")
    data = crud.create_user(db=db, user=user)
    return responses.JSONResponse(content={
        "message": "User created successfully",
        "user": {
            "user_id": data.user_id,
            "name": data.name,
            "email": data.email
        }
    }, status_code=201)


@router.post("/upload-img")
@hash.check_authorization
async def upload_img(request: Request, uploaded_file: UploadFile):
    file_location = f"img/{uploaded_file.filename}"
    contents = await uploaded_file.read()
    
    with open(file_location, "wb+") as file_object:
        file_object.write(contents)
        
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


@router.post("/auth/login")
async def login_user(user: Schemas.UserLogin, db: Session = Depends(get_db)):
    if crud.authenticate_user(db, user.email, user.password) is False:
        return responses.JSONResponse(content={
            "message": "Invalid credentials"
        }, status_code=401)
        
    access_token_expires = timedelta(minutes=5)
    access_token = hash.create_access_token(
        data= {
            "sub": user.email
        },
        expires_delta = access_token_expires
    )
    
    return responses.JSONResponse(content={
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }, status_code=200)