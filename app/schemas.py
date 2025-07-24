# Pydantic models

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    
    model_Config = {
        "from_attributes": True # Required in Pydantic v2 (was `orm_mode = True` in v1)
    }