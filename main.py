from fastapi import FastAPI, HTTPException, Depends
from api.users import users

app = FastAPI()
app.include_router(users.router)


@app.get("/")
async def home():
    return {"message": "Welcome to my FastAPI!"}


