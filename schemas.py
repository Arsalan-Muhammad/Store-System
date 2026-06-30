from xmlrpc.client import boolean
from pydantic import BaseModel
from database import Base
from typing import Optional

class CreateProduct(BaseModel):
    name: str
    price : float
    category : str
    quantity: int

class updateproduct(BaseModel):
    price : float
    quantity : int

class TokenData(BaseModel):
    id : Optional[int] = None    
