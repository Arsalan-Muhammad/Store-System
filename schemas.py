from turtle import st
from unicodedata import category
from xmlrpc.client import boolean

from pydantic import BaseModel
from .database import Base
class CreateProduct(Base):
    name: str
    price : bool
    category : str
    quantity: int