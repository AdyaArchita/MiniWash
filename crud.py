import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
from schemas import OrderCreate, OrderStatus, OrderStatusUpdate

def create_order(db: Session, order_data: OrderCreate) -> models.Order:
    # Calculate total bill
    total_bill = sum(item.quantity * item.price_per_item for item in order_data.garments)
    
    # Generate UUID and check unique (implied in SQLite primary key index but explicit here)
    order_id = str(uuid.uuid4())
    
    # Create the Order object
    db_order = models.Order(
        order_id=order_id,
        customer_name=order_data.customer_name,
        phone=order_data.phone,
        total_bill=round(total_bill, 2),
        status=OrderStatus.RECEIVED,
        created_at=datetime.now(),
        estimated_delivery_date=None
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create Garment objects
    for item in order_data.garments:
        db_garment = models.Garment(
            order_id=order_id,
            type=item.type,
            quantity=item.quantity,
            price_per_item=item.price_per_item
        )
        db.add(db_garment)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(
    db: Session,
    status: Optional[OrderStatus] = None,
    customer_name: Optional[str] = None,
    phone: Optional[str] = None,
    garment_type: Optional[str] = None
) -> List[models.Order]:
    query = db.query(models.Order)
    
    if status:
        query = query.filter(models.Order.status == status)
    
    if customer_name:
        query = query.filter(models.Order.customer_name.ilike(f"%{customer_name}%"))
        
    if phone:
        query = query.filter(models.Order.phone.contains(phone))
        
    if garment_type:
        # Bonus: Join with Garments to filter by type
        query = query.join(models.Garment).filter(models.Garment.type.ilike(f"%{garment_type}%"))
        
    return query.all()

def get_order_by_id(db: Session, order_id: str) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.order_id == order_id).first()

def update_order_status(db: Session, order_id: str, status_update: OrderStatusUpdate) -> Optional[models.Order]:
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
    
    db_order.status = status_update.status
    
    # Bonus: Set estimated delivery date (created_at + 3 days) when status becomes READY
    if status_update.status == OrderStatus.READY:
        db_order.estimated_delivery_date = db_order.created_at + timedelta(days=3)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_dashboard_stats(db: Session) -> dict:
    orders = db.query(models.Order).all()
    total_orders = len(orders)
    total_revenue = sum(order.total_bill for order in orders)
    
    # Initialize status counts
    status_counts = {status: 0 for status in OrderStatus}
    for order in orders:
        status_counts[order.status] += 1
        
    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "orders_per_status": status_counts
    }
