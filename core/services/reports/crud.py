from sqlalchemy.orm import Session, joinedload
from models.reports import Reports
from models.categories import Categories
from fastapi import HTTPException

def get_all_report(db: Session):
    return db.query(Reports).join(Reports.owner).filter(Reports.owner.has(is_deleted=False)).options(joinedload(Reports.owner), joinedload(Reports.category)).all()

def get_report_by_id(db: Session, report_id: int):
    return db.query(Reports).join(Reports.owner).filter(Reports.owner.has(is_deleted=False)).options(joinedload(Reports.owner), joinedload(Reports.category)).filter(Reports.report_id == report_id).first()



def validate_category(db: Session, category_id: int):
    categories = db.query(Categories.category_id, Categories.name).all()
    valid_category_id = [cat.category_id for cat in categories]

    if category_id not in valid_category_id:
        available = [f"{cat.category_id} - {cat.name}" for cat in categories]
        raise HTTPException(
            status_code=400, 
            detail={
                "message": "Category not found",
                "available_categories": available
            }
        )

def create_report(db: Session, report_data: dict, user_id: int):
    validate_category(db, report_data["category_id"])
    
    data = Reports(
        user_id = user_id,
        category_id = report_data["category_id"],
        image_path = report_data["image_path"],
        body = report_data["body"]
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    
    return data