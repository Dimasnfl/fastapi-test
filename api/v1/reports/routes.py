from fastapi import APIRouter, Depends, HTTPException, UploadFile, Request, File, Form
from sqlalchemy.orm import Session
from database.db import get_db
from schemas import reports as Schemas
from core.services.reports import crud
from core import security
from models.users import Users
import os, uuid, shutil
from uuid import UUID

router = APIRouter(
    tags=["reports"],
    responses={404: {"message": "Reports not found"}}
)


@router.get("/", response_model=Schemas.GetReportsResponse)
async def get_all_report(
    db: Session = Depends(get_db), 
    current_user: Users = Depends(security.get_current_user)
    ):
    
    data = crud.get_all_report(db)
    reports_response = [Schemas.GetReports.model_validate(report) for report in data] 
    return {
        "message": "List of report",
        "data": reports_response
    }
    
@router.get("/{report_id}", response_model=Schemas.GetReports)
async def get_report_by_id(
    report_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: Users = Depends(security.get_current_user)
    ):
    
    data = crud.get_report_by_id(db, report_id=report_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return data


@router.post("/create-report", response_model=Schemas.GetCreatedReportResponse)
async def create_report(
    db: Session = Depends(get_db), 
    category_id: int = Form(...), body: str = Form(...), image: UploadFile | None = File(None), 
    current_user: Users = Depends(security.get_current_user)
    ):
    
    crud.validate_category(db, category_id)
    
    filename = None
    if image and image.filename:
        os.makedirs("static/img", exist_ok=True)
        file_extension = os.path.splitext(image.filename)[1]
        
        if file_extension.lower() not in [".jpg", ".jpeg", ".png"]:
            raise HTTPException(status_code=400, detail="Image format not allowed. Please use jpg, jpeg, png.")
        
        filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = f"static/img/{filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    data = crud.create_report(
        db=db,
        report_data={
            "category_id": category_id,
            "body": body,
            "image_path": filename
        },
        user_id=current_user.user_id
    )
    reports_response = Schemas.GetCreatedReport.model_validate(data)

    return {
        "message": "Your report created successfully",
        "data": reports_response
    }