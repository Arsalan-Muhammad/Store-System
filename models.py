
from sqlalchemy.sql import text
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Products(Base):
    __tablename__ = "posts"

    name = Column(String, nullable=False)
    price = Column(Boolean , nullable=False)
    category = Column(String , nullable=False)
    quantity = Column(String , nullable=False)