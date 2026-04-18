from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class OrderStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    DELIVERED = "DELIVERED"

class GarmentBase(BaseModel):
    type: str = Field(..., example="Shirt")
    quantity: int = Field(..., gt=0, example=2)
    price_per_item: float = Field(..., gt=0, example=120.0)

class GarmentCreate(GarmentBase):
    pass

class OrderCreate(BaseModel):
    customer_name: str = Field(..., example="John Doe")
    phone: str = Field(..., example="1234567890")
    garments: List[GarmentCreate]

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(BaseModel):
    order_id: UUID
    customer_name: str
    phone: str
    garments: List[GarmentBase]
    total_bill: float
    status: OrderStatus
    created_at: datetime
    estimated_delivery_date: Optional[datetime] = None

class DashboardResponse(BaseModel):
    total_orders: int
    total_revenue: float
    orders_per_status: dict[OrderStatus, int]
