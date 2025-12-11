from __future__ import annotations

import os
import socket
from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware

from utils.pubsub_events import publish_new_record_trigger

from fastapi import Depends, FastAPI, HTTPException, Path, Query
import uvicorn
from models.booking import BookingCreate, BookingRead, BookingUpdate
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


@app.get("/bookings/all", response_model=list[BookingRead])
def list_all_bookings(conn = Depends(get_db)):
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
                           SELECT * 
                           FROM bookings 
                       """)
        
        bookings = cursor.fetchall()
        
        if not bookings:
            raise HTTPException(status_code = 404, detail = "No bookings found")

        return bookings
        
    finally:
        cursor.close()


@app.get("/bookings/tenant/{tenant_email}", response_model=list[BookingRead])
def list_bookings_by_user(tenant_email: str, conn=Depends(get_db)):

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
                           SELECT * 
                           FROM bookings 
                           WHERE tenant_email = %s
                       """, (tenant_email,))
        
        bookings = cursor.fetchall()
        
        if not bookings:
            raise HTTPException(status_code = 404, detail = "No bookings found")


        return bookings
        
    finally:
        cursor.close()

@app.get("/bookings/listing/{listing_id}", response_model=list[BookingRead])
def list_bookings_by_listing(listing_id: int, conn = Depends(get_db)):
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
                           SELECT * 
                           FROM bookings 
                           WHERE listing_id = %s
                       """, (listing_id,))
        
        bookings = cursor.fetchall()
        
        if not bookings:
            raise HTTPException(status_code = 404, detail = "No bookings found")

        return bookings
        
    finally:
        cursor.close()

@app.post("/bookings", status_code=201, response_model=BookingRead)
def create_booking(payload: BookingCreate, conn = Depends(get_db)):
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            INSERT INTO bookings (listing_id, tenant_email, start_date, end_date)
            VALUES (%s, %s, %s, %s)
            """,
            (
                payload.listing_id,
                payload.tenant_email,
                payload.start_date,
                payload.end_date,
            ),
        )

        conn.commit()

        new_id = cursor.lastrowid

        # Publish Pub/Sub event after DB commit
        try:
            publish_new_record_trigger(
                record_id=str(new_id),
                client_name=payload.tenant_email, 
            )
        except Exception as e:
            # Log but do not fail the request
            print(f"Pub/Sub error (ignored): {e}")

        cursor.execute(
            """
            SELECT id, listing_id, tenant_email, start_date, end_date
            FROM bookings
            WHERE id = %s
            """,
            (new_id,),
        )
        new_booking = cursor.fetchone()

        return new_booking

    finally:
        cursor.close()



@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int, conn=Depends(get_db)):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE 
            FROM bookings
            WHERE id = %s
            """,
            (booking_id,),)
        
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Booking not found")

        # 204 = No Content → return nothing
        return None

    finally:
        cursor.close()

@app.put("/bookings/update/{booking_id}", response_model=BookingRead)
def update_booking(
    booking_id: int,
    payload: BookingUpdate,     
    conn = Depends(get_db),
):
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM bookings WHERE id = %s",
            (booking_id,),
        )
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Booking not found")

        updated_start = payload.start_date or existing["start_date"]
        updated_end = payload.end_date or existing["end_date"]

        cursor.execute(
            """
            UPDATE bookings
            SET start_date = %s,
                end_date = %s
            WHERE id = %s
            """,
            (updated_start, updated_end, booking_id),
        )
        conn.commit()

        cursor.execute(
            """
            SELECT id, listing_id, tenant_email, start_date, end_date
            FROM bookings
            WHERE id = %s
            """,
            (booking_id,),
        )
        return cursor.fetchone()

    finally:
        cursor.close()

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
