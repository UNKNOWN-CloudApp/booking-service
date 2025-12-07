from __future__ import annotations

import os
import socket
from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware


from fastapi import Depends, FastAPI, HTTPException, Path, Query
import uvicorn
from models.booking import BookingCreate, BookingRead
from utils.database import get_db

port = int(os.environ.get("PORT") or os.environ.get("FASTAPIPORT", 8080))

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

# mock version
USE_MOCK = True

@app.get("/bookings/all", response_model=list[BookingRead])
def list_all_bookings(conn = Depends(get_db)):
    if USE_MOCK:
        return [
            BookingRead(
                id=1,
                listing_id= 1,
                tenant_email= "david.lee@example.com",
                start_date="2025-04-01",
                end_date="2025-04-05",
            ),
            BookingRead(
                id=2,
                listing_id= 3,
                tenant_email= "eva.chen@example.com",
                start_date="2025-05-10",
                end_date="2025-05-15",
            )
        ]

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

@app.get("/bookings/{tenant_email}", response_model=list[BookingRead])
def list_bookings_by_user(tenant_email: str, conn=Depends(get_db)):
    if USE_MOCK:
        return [
            BookingRead(
                id=1,
                listing_id= 1,
                tenant_email= "david.lee@example.com",
                start_date="2025-06-01",
                end_date="2025-06-07",
            )
        ]

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
                           SELECT * 
                           FROM bookings 
                           WHERE tenentID = %s
                       """)
        
        bookings = cursor.fetchall()
        
        if not bookings:
            return {"message": "No bookings found"}

        return bookings
        
    finally:
        cursor.close()

@app.get("/bookings/{listing_id}")
def list_bookings_by_listing(listing_id: str, conn = Depends(get_db)):
    if USE_MOCK:
        return [
            {
                "id": 1,
                "listing_id": 1,
                "tenant_email": "david.lee@example.com",
                "start_date": "2025-06-01",
                "end_date": "2025-06-05"
            },
            {
                "id": 2,
                "listing_id": 3,
                "tenant_email": "eva.chen@example.com",
                "start_date": "2025-07-10",
                "end_date": "2025-07-12"
            }
        ]
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
                           SELECT * 
                           FROM bookings 
                           WHERE listing_id = %s
                       """)
        
        bookings = cursor.fetchall()
        
        if not bookings:
            return {"message": "No bookings found"}

        return bookings
        
    finally:
        cursor.close()

@app.post("/bookings", status_code=201)
def create_booking(payload: BookingCreate):
    if USE_MOCK:
        return BookingRead(
            id=3,
            listing_id=payload.listing_id,
            tenant_email=payload.tenant_email,
            start_date=payload.start_date,
            end_date=payload.end_date,
        )

    cursor = conn.cursor(dictionary=True)

    try:
        booking_id = uuid4()

        cursor.execute(
            """
            INSERT INTO Booking (ID, listing_id, tenant_email, start_date, end_date)
            """,
            (
                str(booking_id),
                str(payload.listing_id),
                payload.tenant_email,
                payload.start_date,
                payload.end_date,
            ),
        )
        
    finally:
        cursor.close()

@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int, conn=Depends(get_db)):
    if USE_MOCK:
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM Booking WHERE ID = %s
            """,
            (str(booking_id),)
        )
        conn.commit()

        if cursor.rowcount == 0:
            # No booking deleted → booking doesn't exist
            raise HTTPException(status_code=404, detail="Booking not found")

        # 204 = No Content → return nothing
        return

    finally:
        cursor.close()

@app.put("/bookings/{booking_id}/reject")
def reject_booking(booking_id: UUID):
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
