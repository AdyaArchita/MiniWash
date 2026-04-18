import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from schemas import OrderCreate, OrderStatus, OrderStatusUpdate, OrderResponse, DashboardResponse
from models import orders_db

def create_order(order_data: OrderCreate) -> dict:
    # Calculate total bill
    total_bill = sum(item.quantity * item.price_per_item for item in order_data.garments)
    
    # Create the order object
    new_order = {
        "order_id": uuid.uuid4(),
        "customer_name": order_data.customer_name,
        "phone": order_data.phone,
        "garments": [item.model_dump() for item in order_data.garments],
        "total_bill": round(total_bill, 2),
        "status": OrderStatus.RECEIVED,
        "created_at": datetime.now(),
        "estimated_delivery_date": None
    }
    
    orders_db.append(new_order)
    return new_order

def get_orders(
    status: Optional[OrderStatus] = None,
    customer_name: Optional[str] = None,
    phone: Optional[str] = None,
    garment_type: Optional[str] = None
) -> List[dict]:
    filtered_orders = orders_db
    
    if status:
        filtered_orders = [o for o in filtered_orders if o["status"] == status]
    
    if customer_name:
        filtered_orders = [o for o in filtered_orders if customer_name.lower() in o["customer_name"].lower()]
        
    if phone:
        filtered_orders = [o for o in filtered_orders if phone in o["phone"]]
        
    if garment_type:
        # Bonus: Filter by garment type in any of the garments in the order
        filtered_orders = [
            o for o in filtered_orders 
            if any(garment_type.lower() in g["type"].lower() for g in o["garments"])
        ]
        
    return filtered_orders

def get_order_by_id(order_id: uuid.UUID) -> Optional[dict]:
    for order in orders_db:
        if order["order_id"] == order_id:
            return order
    return None

def update_order_status(order_id: uuid.UUID, status_update: OrderStatusUpdate) -> Optional[dict]:
    order = get_order_by_id(order_id)
    if not order:
        return None
    
    order["status"] = status_update.status
    
    # Bonus: Set estimated delivery date (created_at + 3 days) when status becomes READY
    if status_update.status == OrderStatus.READY:
        order["estimated_delivery_date"] = order["created_at"] + timedelta(days=3)
        
    return order

def get_dashboard_stats() -> dict:
    total_orders = len(orders_db)
    total_revenue = sum(order["total_bill"] for order in orders_db)
    
    # Initialize status counts
    status_counts = {status: 0 for status in OrderStatus}
    for order in orders_db:
        status_counts[order["status"]] += 1
        
    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "orders_per_status": status_counts
    }
