
from sqlalchemy.sql import text
from database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean , Float
from sqlalchemy.orm import relationship

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer , nullable=False , primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float , nullable=False , default=0)
    category = Column(String , nullable=False)
    quantity = Column(Integer , nullable=False)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String , nullable=False , unique=True)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)     