#!/bin/bash

# Mini Laundry Order Management System - Runner Script

echo "Checking dependencies..."
pip install -r requirements.txt

echo "Starting FastAPI server on http://127.0.0.1:8000"
echo "API Documentation available at http://127.0.0.1:8000/docs"

uvicorn main:app --reload
