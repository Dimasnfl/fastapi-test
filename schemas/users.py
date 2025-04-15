from pydantic import BaseModel
from typing import List
from uuid import UUID


class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    
class BaseUser(BaseSchema):
    email: str
    
    
# show users
class GetUsers(BaseUser):
    name: str
    user_id: UUID
    
class GetUsersResponse(BaseSchema):
    message: str
    data: List[GetUsers]
    

# create user
class CreateUser(BaseUser):
    name: str
    password: str
    
    
# show created user
class GetCreatedUser(BaseUser):
    name: str
    user_id: UUID

class GetCreatedUserResponse(BaseSchema):
    message: str
    data: GetCreatedUser


# input email&password
class LoginUser(BaseUser):
    password: str
    
