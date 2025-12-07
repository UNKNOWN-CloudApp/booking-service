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
                id="11111111-2222-3333-4444-555555555555",
                listingID="aaaa1111-bbbb-2222-cccc-333333333333",
                tenantID="mock-user-123",
                start_date="2025-04-01",
                end_date="2025-04-05",
            ),
            BookingRead(
                id="22222222-3333-4444-5555-666666666666",
                listingID="dddd4444-eeee-5555-ffff-666666666666",
                tenantID="mock-user-123",
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

@app.get("/bookings/{tenantID}", response_model=list[BookingRead])
def list_bookings_by_user(tenantID: str, conn=Depends(get_db)):
    if USE_MOCK:
        return [
            BookingRead(
                id="99999999-aaaa-bbbb-cccc-dddddddddddd",
                listingID="aaaa1111-bbbb-2222-cccc-333333333333",
                tenantID=tenantID,
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

@app.get("/bookings/{listingID}")
def list_bookings_by_listing(listingID: str, conn = Depends(get_db)):
    if USE_MOCK:
        return [
            {
                "id": "mock-booking-1",
                "listingID": listingID,     
                "tenantID": "mock-user-123",
                "start_date": "2025-06-01",
                "end_date": "2025-06-05"
            },
            {
                "id": "mock-booking-2",
                "listingIID": listingID,
                "tenantenantIDt_id": "mock-user-456",
                "start_date": "2025-07-10",
                "end_date": "2025-07-12"
            }
        ]
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
                           SELECT * 
                           FROM bookings 
                           WHERE listingID = %s
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
            id="11111111-2222-3333-4444-555555555555",
            listingID=payload.listingID,
            tenantID=payload.tenantID,
            start_date=payload.start_date,
            end_date=payload.end_date,
        )

    cursor = conn.cursor(dictionary=True)

    try:
        booking_id = uuid4()

        cursor.execute(
            """
            INSERT INTO Booking (ID, ListingID, TenantID, start_date, end_date)
            """,
            (
                str(booking_id),
                str(payload.listingID),
                payload.tenantID,
                payload.start_date,
                payload.end_date,
            ),
        )
        
    finally:
        cursor.close()

@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: UUID, conn=Depends(get_db)):
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
