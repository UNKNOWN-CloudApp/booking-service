from __future__ import annotations

from typing import Optional, Literal
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class BookingBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Booking ID (server-generated).",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    listing_id: UUID = Field(
        ...,
        description="ID of the listing being booked.",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    tenant_id: UUID = Field(
        ...,
        description="ID of the tenant requesting the booking.",
        json_schema_extra={"example": "111e8400-e29b-41d4-a716-446655440999"},
    )
    landlord_id: UUID = Field(
        ...,
        description="ID of the landlord who owns the listing.",
        json_schema_extra={"example": "222e8400-e29b-41d4-a716-446655440888"},
    )
    status: Literal["pending", "accepted", "rejected"] = Field(
        "pending",
        description="Booking status.",
        json_schema_extra={"example": "pending"},
    )
    start_date: datetime = Field(
        ...,
        description="Start date/time of the rental period (UTC).",
        json_schema_extra={"example": "2025-05-01T14:00:00Z"},
    )
    end_date: datetime = Field(
        ...,
        description="End date/time of the rental period (UTC).",
        json_schema_extra={"example": "2025-05-15T11:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "listing_id": "550e8400-e29b-41d4-a716-446655440000",
                    "tenant_id": "111e8400-e29b-41d4-a716-446655440999",
                    "landlord_id": "222e8400-e29b-41d4-a716-446655440888",
                    "status": "pending",
                    "start_date": "2025-05-01T14:00:00Z",
                    "end_date": "2025-05-15T11:00:00Z",
                }
            ]
        }
    }


class BookingCreate(BookingBase):
    """Creation payload; ID is generated server-side but present in the base model."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "listing_id": "550e8400-e29b-41d4-a716-446655440000",
                    "tenant_id": "111e8400-e29b-41d4-a716-446655440999",
                    "landlord_id": "222e8400-e29b-41d4-a716-446655440888",
                    "status": "pending",
                    "start_date": "2025-05-01T14:00:00Z",
                    "end_date": "2025-05-15T11:00:00Z",
                }
            ]
        }
    }


class BookingUpdate(BaseModel):
    """Partial update; booking ID is taken from the path, not the body."""
    status: Optional[Literal["pending", "accepted", "rejected"]] = Field(
        None,
        description="Updated booking status.",
        json_schema_extra={"example": "accepted"},
    )
    start_date: Optional[datetime] = Field(
        None,
        description="Updated start date/time.",
        json_schema_extra={"example": "2025-05-02T10:00:00Z"},
    )
    end_date: Optional[datetime] = Field(
        None,
        description="Updated end date/time.",
        json_schema_extra={"example": "2025-05-16T11:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": "accepted"},
                {
                    "start_date": "2025-05-02T10:00:00Z",
                    "end_date": "2025-05-16T11:00:00Z",
                },
            ]
        }
    }


class BookingRead(BookingBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-04-10T09:30:00Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-04-12T16:45:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "listing_id": "550e8400-e29b-41d4-a716-446655440000",
                    "tenant_id": "111e8400-e29b-41d4-a716-446655440999",
                    "landlord_id": "222e8400-e29b-41d4-a716-446655440888",
                    "status": "accepted",
                    "start_date": "2025-05-01T14:00:00Z",
                    "end_date": "2025-05-15T11:00:00Z",
                    "created_at": "2025-04-10T09:30:00Z",
                    "updated_at": "2025-04-12T16:45:00Z",
                }
            ]
        }
    }
