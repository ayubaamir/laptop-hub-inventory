from sqlalchemy import Column, Integer, String, Float
from database import Base   # yahan se Base import hoga

# Product class table ka structure define karti hai
class Product(Base):
    __tablename__ = "products"   # PostgreSQL table ka naam

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    quantity = Column(Integer)