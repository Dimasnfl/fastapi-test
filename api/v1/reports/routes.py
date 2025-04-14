from fastapi import APIRouter, Depends, HTTPException, UploadFile, responses, Request
from sqlalchemy.orm import Session
from database.db import get_db
from schemas import reports as Schemas
from core.services.reports import crud

router = APIRouter(
    tags=["reports"],
    responses={404: {"message": "Reports not found"}}
)


@router.get("/", response_model=Schemas.GetReportsResponse)
async def get_all_report(db: Session = Depends(get_db)):
    data = crud.get_all_report(db)
    reports_response = [Schemas.GetReports.model_validate(report) for report in data] 
    return {
        "message": "List of reports",
        "data": reports_response
    }