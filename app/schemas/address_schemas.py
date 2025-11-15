from pydantic import BaseModel, Field
from typing import Optional


class AddressCreate(BaseModel):
    full_name: str
    phone_number: str

    address_type: str = Field(default="Home", description="Home, Work, Other")
    is_default: bool = Field(default=False, description="Set as default address for checkout")

    country: str = Field(default="Nepal")
    province: str
    district: str
    city: str
    tole: Optional[str] = None
    landmark: Optional[str] = Field(default=None, description="e.g., Near Sajha Park")

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "phone_number": "9841234567",
                "address_type": "Home",
                "is_default": True,
                "country": "Nepal",
                "province": "Bagmati",
                "district": "Kathmandu",
                "city": "Kathmandu",
                "tole": "Dillibazar",
                "landmark": "Near Sajha Park"
            }
        }


class AddressUpdate(BaseModel):

    full_name: Optional[str] = None
    phone_number: Optional[str] = None

    address_type: Optional[str] = None
    is_default: Optional[bool] = None

    country: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    tole: Optional[str] = None
    landmark: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "9851234567",
                "landmark": "Near New Buspark"
            }
        }


class AddressResponse(BaseModel):
    full_name: str
    phone_number: str

    address_type: str
    is_default: bool
    
    country: str
    province: str
    district: str
    city: str
    tole: Optional[str] = None
    landmark: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "phone_number": "9841234567",
                "address_type": "Home",
                "is_default": True,
                "country": "Nepal",
                "province": "Bagmati",
                "district": "Kathmandu",
                "city": "Kathmandu",
                "tole": "Dillibazar",
                "landmark": "Near Sajha Park"
            }
        }
