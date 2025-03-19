

from sqlalchemy import Column, Integer, String
from database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(String, nullable=False)
    category = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    upc = Column(String, unique=True, nullable=False)
    availability = Column(String, nullable=False)
    in_stock = Column(Integer, nullable=False)
    image_link = Column(String, nullable=False)
