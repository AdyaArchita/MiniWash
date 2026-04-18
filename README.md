# Mini Laundry Order Management System (AI-First)

A lightweight FastAPI-driven order management system for a small dry cleaning business. Built with speed, correctness, and clean code in mind.

## 🚀 Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```

3. **API Documentation**:
   Once the server is running, visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## ✅ Features Implemented

- [x] **New: Dashboard UI (Included!)**: A high-end single-page dashboard with Dark Mode and Glassmorphism for better visualization.
- [x] **Create Order (POST `/orders`)**: Auto-calculates total bill, generates UUID, and sets "RECEIVED" status.
- [x] **Update Order Status (PATCH `/orders/{id}/status`)**: Validates status transitions and handles business logic.
- [x] **View Orders (GET `/orders`)**: Filter by status, customer name (partial), phone (partial), or garment type (bonus).
- [x] **Single Order Detail (GET `/orders/{id}`)**: Fetch full order object.
- [x] **Dashboard (GET `/dashboard`)**: Total orders, total revenue, and status breakdown.
- [x] **Bonus: Estimated Delivery Date**: Automatically sets `created_at + 3 days` when status becomes "READY".
- [x] **Bonus: Garment Type Search**: Search orders containing specific garment types (e.g., "Saree").

---

## 🧪 Sample Curl Commands / Test Examples

### 1. Create Order
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/orders' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer_name": "Adya Archita",
  "phone": "9876543210",
  "garments": [
    {"type": "Shirt", "quantity": 2, "price_per_item": 120},
    {"type": "Pants", "quantity": 1, "price_per_item": 150}
  ]
}'
```

---

## 🏗️ Project Structure
```
laundry-order-system/
├── main.py          # API Endpoints & FastAPI App
├── schemas.py       # Pydantic Data Models (V2)
├── models.py        # In-memory data store setup
├── crud.py          # Business Logic & Data Operations
├── requirements.txt # Dependencies
├── run.sh           # One-click startup script
└── README.md        # Documentation
```

---

## ⚖️ Tradeoffs
- **Persistence**: Used in-memory storage (list) for speed. Data resets on server restart. A production system would use PostgreSQL/SQLAlchemy.
- **Auth**: Authentication was skipped to focus on the core system logic.
- **Error Handling**: Basic 404/422 handling is implemented; complex validation logic could be moved to domain-specific validators.

## 🔮 Future Improvements
- Add persistent database storage (SQLAlchemy/Ariel/MongoDB).
- Implement JWT-based authentication for staff.
- Add "Customer History" endpoint.
- Web-based Dashboard using React/Next.js.

---

## 🔹 AI Usage Report

- **Tools Used**: Antigravity (Google Deepmind AI Assistance)
- **Sample Prompts**:
  - "Build a Mini Laundry Order Management System with FastAPI and Pydantic v2."
  - "Create a single-file modern dashboard UI with glassmorphism for this API."
  - "Generate a Postman collection for a laundry management system."
- **What AI Got Wrong**: 
  - Initially suggested relative imports (`from .schemas`) which caused issues when running `uvicorn main:app` directly from the parent directory without a package structure. 
  - The first draft of the UI didn't have auto-refresh for statistics, which I added to make the demo feel more "alive".
- **What I Improved**:
  - Refactored imports to support flat-directory execution.
  - Enhanced the UI with `backdrop-filter` for a premium glassmorphism effect.
  - Implemented the `estimated_delivery_date` logic precisely inside the status update flow.

---
*Created for the MiniWash Technical Assessment.*