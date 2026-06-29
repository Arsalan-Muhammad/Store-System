from xmlrpc.client import boolean
from pydantic import BaseModel
from database import Base
class CreateProduct(BaseModel):
    name: str
    price : float
    category : str
    quantity: int