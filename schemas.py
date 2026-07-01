from xmlrpc.client import boolean
from pydantic import BaseModel
from database import Base
from typing import Optional
from pydantic import EmailStr
from datetime import datetime
class CreateProduct(BaseModel):
    name: str
    price : float
    category : Optional[str]
    quantity: int

class updateproduct(BaseModel):
    price : float
    quantity : int

class TokenData(BaseModel):
    id : Optional[int] = None    

class UserCreate(BaseModel):
    email: EmailStr
    password: str    

class UserOut(BaseModel):
    id: int
    email: EmailStr  
    created_at: datetime

    class Config:
        orm_mode = True 

