from __future__ import annotations

from typing import Optional, Literal
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class BookingBase(BaseModel):
    ID: UUID = Field(
        default_factory=uuid4,
        description="Persistent Booking ID (server-generated).",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    listingID: UUID = Field(
        ...,
        description="ID of the listing being booked.",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    tenantID: str = Field(
        ...,
        description="ID of the tenant requesting the booking.",
        json_schema_extra={"example": "111e8400-e29b-41d4-a716-446655440999"},
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
                    "ID": "123e4567-e89b-12d3-a456-426614174000",
                    "listingID": "550e8400-e29b-41d4-a716-446655440000",
                    "tenantID": "111e8400-e29b-41d4-a716-446655440999",
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
                    "listingID": "550e8400-e29b-41d4-a716-446655440000",
                    "tenantID": "111e8400-e29b-41d4-a716-446655440999",
                    "start_date": "2025-05-01T14:00:00Z",
                    "end_date": "2025-05-15T11:00:00Z",
                }
            ]
        }
    }


class BookingUpdate(BaseModel):
    """Partial update; booking ID is taken from the path, not the body."""
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
                {
                    "start_date": "2025-05-02T10:00:00Z",
                    "end_date": "2025-05-16T11:00:00Z",
                },
            ]
        }
    }

class BookingRead(BookingBase):
    id: UUID

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ID": "123e4567-e89b-12d3-a456-426614174000",
                    "listingID": "550e8400-e29b-41d4-a716-446655440000",
                    "tenantID": "111e8400-e29b-41d4-a716-446655440999",
                    "start_date": "2025-05-01T14:00:00Z",
                    "end_date": "2025-05-15T11:00:00Z",
                    "created_at": "2025-04-10T09:30:00Z",
                    "updated_at": "2025-04-12T16:45:00Z",
                }
            ]
        }
    }

    