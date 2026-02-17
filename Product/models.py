from sqlalchemy import Column, Float, Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    seller=relationship("Seller", back_populates="products")

class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    products = relationship("Product", back_populates="seller")