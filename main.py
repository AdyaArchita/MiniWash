from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import List, Optional
from uuid import UUID

from schemas import OrderCreate, OrderStatus, OrderStatusUpdate, OrderResponse, DashboardResponse
import crud

app = FastAPI(
    title="Mini Laundry Order Management System",
    description="A simple API for managing dry cleaning store orders.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate):
    """Create a new laundry order."""
    return crud.create_order(order)

@app.get("/orders", response_model=List[OrderResponse])
def read_orders(
    status: Optional[OrderStatus] = Query(None, description="Filter by exact status"),
    customer_name: Optional[str] = Query(None, description="Partial match for customer name"),
    phone: Optional[str] = Query(None, description="Partial match for phone number"),
    garment_type: Optional[str] = Query(None, description="Filter by garment type (e.g., Shirt)")
):
    """List all orders with optional filtering."""
    return crud.get_orders(status, customer_name, phone, garment_type)

@app.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: UUID):
    """Get a single order by its ID."""
    order = crud.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: UUID, status_update: OrderStatusUpdate):
    """Update the status of an existing order."""
    order = crud.update_order_status(order_id, status_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/dashboard", response_model=DashboardResponse)
def get_dashboard():
    """Get summarized statistics for the store."""
    return crud.get_dashboard_stats()

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint: Redirect to the UI dashboard
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/static/index.html")
