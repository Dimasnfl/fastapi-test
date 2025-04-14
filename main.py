from fastapi import FastAPI
from api.v1.users import routes as user_routes
from api.v1.reports import routes as reports_routes

app = FastAPI()
app.include_router(user_routes.router, prefix="/api/v1/users")
app.include_router(reports_routes.router, prefix="/api/v1/reports")


@app.get("/")
async def home():
    return {"message": "Welcome to my FastAPI!"}


