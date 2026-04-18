from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
import enum
from schemas import OrderStatus
import uuid

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    phone = Column(String, index=True)
    total_bill = Column(Float)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.RECEIVED)
    created_at = Column(DateTime)
    estimated_delivery_date = Column(DateTime, nullable=True)

    garments = relationship("Garment", back_populates="order", cascade="all, delete-orphan")

class Garment(Base):
    __tablename__ = "garments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.order_id"))
    type = Column(String)
    quantity = Column(Integer)
    price_per_item = Column(Float)

    order = relationship("Order", back_populates="garments")
