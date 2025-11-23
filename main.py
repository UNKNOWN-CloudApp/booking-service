from __future__ import annotations

import os
import socket
from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware


from fastapi import Depends, FastAPI, HTTPException, Path, Query
import uvicorn

from utils.database import get_db

port = int(os.environ.get("PORT") or os.environ.get("FASTAPIPORT", 8000))

app = FastAPI(
    title="Booking Service",
    description="Booking microservice",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------------------------------------------
# Booking endpoints
# -----------------------------------------------------------------------------
@app.post("/bookings", status_code=201)
def create_booking():
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.get("/bookings")
def list_bookings(conn = Depends(get_db)):
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
                           SELECT * 
                           FROM bookings 
                       """)
        
        bookings = cursor.fetchall()
        
        if not bookings:
            return {"message": "No bookings found"}

        return bookings
        
    finally:
        cursor.close()

@app.get("/bookings/{booking_id}")
def get_booking(booking_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.patch("/bookings/{booking_id}")
def update_booking(booking_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.put("/bookings/{booking_id}/confirm")
def confirm_booking(booking_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.put("/bookings/{booking_id}/reject")
def reject_booking(booking_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.get("/tenants/{tenant_id}/bookings")
def list_bookings_for_tenant(tenant_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.get("/landlords/{landlord_id}/bookings")
def list_bookings_for_landlord(landlord_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented yet")

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Booking Service"}

# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
