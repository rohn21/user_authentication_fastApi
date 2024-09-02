from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional
import uuid

class UserModel(BaseModel):
    # id:str = Field(default_factory=uuid.uuid4, alias="_id")
    # id:str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id", convert_raw=True)
    username: str
    email: EmailStr
    password: str
    linked_id: Optional[str] = None
    
    class config:
        orm_mode = True
        schema_extra = {"exclude": ["linked_id"]}

class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
    
class LinkIdModel(BaseModel):
    email: EmailStr
    linked_id: str
    
    
# class UserUpdateModel(BaseModel):
#     username: None
#     email: EmailStr = None
#     password: Nonex