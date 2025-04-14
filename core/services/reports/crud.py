from sqlalchemy.orm import Session, joinedload
from models.reports import Reports
from schemas import reports as schemas

def get_all_report(db: Session):
    return db.query(Reports).join(Reports.owner).filter(Reports.owner.has(is_deleted=False)).options(joinedload(Reports.owner), joinedload(Reports.category)).all()