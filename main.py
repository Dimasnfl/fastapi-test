from fastapi import FastAPI, HTTPException, Depends
from api.v1.users import routes as user_routes

app = FastAPI()
app.include_router(user_routes.router, prefix="/api/v1/users")


@app.get("/")
async def home():
    return {"message": "Welcome to my FastAPI!"}


