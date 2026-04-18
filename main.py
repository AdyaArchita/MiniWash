from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets
from typing import List, Optional

import crud
import models
from database import engine, get_db
from schemas import OrderCreate, OrderStatus, OrderStatusUpdate, OrderResponse, DashboardResponse

# Create Database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Laundry Order Management System",
    description="A simple API for managing dry cleaning store orders with Persistence and Auth.",
    version="1.1.0"
)

# Admin Credentials (Hardcoded for Demo)
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = ADMIN_USER.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = ADMIN_PASS.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Public: Create a new laundry order."""
    return crud.create_order(db, order)

@app.get("/orders", response_model=List[OrderResponse])
def read_orders(
    status: Optional[OrderStatus] = Query(None),
    customer_name: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    garment_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List orders (Public for demo, can be protected)"""
    return crud.get_orders(db, status, customer_name, phone, garment_type)

@app.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: str, db: Session = Depends(get_db)):
    """Get a single order by its ID."""
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str, 
    status_update: OrderStatusUpdate, 
    db: Session = Depends(get_db),
    username: str = Depends(authenticate_user)
):
    """Protected: Update order status (Admin only)."""
    order = crud.update_order_status(db, order_id, status_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), username: str = Depends(authenticate_user)):
    """Protected: Get business metrics (Admin only)."""
    return crud.get_dashboard_stats(db)

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint: Redirect to the UI dashboard
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/static/index.html")
