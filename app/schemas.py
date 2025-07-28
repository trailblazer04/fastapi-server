# Pydantic models

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    address: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: str
    
    class Config:
        orm_mode = True


# Not Required when using SQLModel