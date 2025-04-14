from pydantic import BaseModel
from typing import List, Optional


class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }

# relationship scheme of reports to users
class ReportUser(BaseSchema):
    user_id: int
    name: str
    email: str

# relationship scheme of reports to users
class ReportCategory(BaseSchema):
    category_id: int
    name: str

# show all report
class GetReports(BaseSchema):
    report_id: int
    owner: ReportUser
    category: ReportCategory
    image_path: Optional[str]
    body: str
    
class GetReportsResponse(BaseSchema):
    message: str
    data: List[GetReports]
    
    
# create report
class CreateReport(BaseSchema):
    category_id: int
    body: str
    image_path: Optional[str]
    
    
# show created report
class GetCreatedReport(BaseSchema):
    report_id: int
    image_path: Optional[str]
    body: str

class GetCreatedReportResponse(BaseSchema):
    message: str
    data: GetCreatedReport
