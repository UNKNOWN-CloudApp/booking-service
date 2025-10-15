from __future__ import annotations

import os
import socket
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException, Path, Query
import uvicorn

from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

app = FastAPI(
    title="Booking Service",
    description="Booking microservice (stubbed endpoints).",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Health
# -----------------------------------------------------------------------------
def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo,
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: Optional[str] = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: Optional[str] = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# -----------------------------------------------------------------------------
# Booking endpoints
# -----------------------------------------------------------------------------
@app.post("/bookings", status_code=201)
def create_booking():
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.get("/bookings")
def list_bookings():
    raise HTTPException(status_code=501, detail="Not implemented yet")

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
    return {"message": "Booking Service (endpoints not implemented yet)"}

# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
