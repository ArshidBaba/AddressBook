from typing import Any
from typing_extensions import Self
from pydantic import BaseModel, field_validator, ConfigDict

class AddressBase(BaseModel):
    label: str
    street: str
    city: str
    state: str | None = None
    zip_code: str | None = None
    country: str = "IN"
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    """Schema for creating a new address - all fields required except optionals."""

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, latitude: float) -> float:
        if not -90 <= latitude <=90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude
    
    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, longitude:float) -> float:
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude
    
class AddressUpdate(BaseModel):
    """Schema for partial address updates."""
    label: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, latitude: float | None) -> float | None:
        if latitude is not None and not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude
    
    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, longitude: float | None) -> float | None:
        if longitude is not None and not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude
        
class Address(AddressBase):
    """Response schema - includes DB-generated ID."""
    id: int

    model_config = ConfigDict(from_attributes=True)