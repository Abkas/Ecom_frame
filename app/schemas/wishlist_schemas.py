from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WishlistItemAdd(BaseModel):

    product_id: str

    notify_on_sale: bool = Field(default=False, description="Notify when product goes on sale")
    notify_on_restock: bool = Field(default=False, description="Notify when back in stock")

    priority: str = Field(default="normal", description="low, normal, high")

    notes: Optional[str] = Field(default=None, max_length=200, description="Personal note")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345",
                "notify_on_sale": True,
                "notify_on_restock": False,
                "priority": "high",
                "notes": "Buy this for birthday gift"
            }
        }


class WishlistItemUpdate(BaseModel):
    product_id: str

    notify_on_sale: Optional[bool] = None
    notify_on_restock: Optional[bool] = None
    priority: Optional[str] = None

    notes: Optional[str] = Field(default=None, max_length=200)

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345",
                "priority": "normal",
                "notes": "Changed my mind, not urgent"
            }
        }


class WishlistItemRemove(BaseModel):
    product_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345"
            }
        }


class WishlistItemResponse(BaseModel):
 
    product_id: str
    product_name: str  # Fetched from product collection
    product_price: float  # Current price

    product_image: Optional[str] = None  # First image
    is_available: bool  # Is product in stock

    added_at: datetime

    notify_on_sale: bool
    notify_on_restock: bool
    priority: str

    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345",
                "product_name": "Wireless Headphones",
                "product_price": 89.99,
                "product_image": "https://example.com/headphones.jpg",
                "is_available": True,
                "added_at": "2025-11-10T14:30:00",
                "notify_on_sale": True,
                "notify_on_restock": False,
                "priority": "high",
                "notes": "Buy this for birthday gift"
            }
        }


class WishlistResponse(BaseModel):
    items: List[WishlistItemResponse]
    total_items: int

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "product_id": "64a1b2c3d4e5f6789012345",
                        "product_name": "Wireless Headphones",
                        "product_price": 89.99,
                        "product_image": "https://example.com/headphones.jpg",
                        "is_available": True,
                        "added_at": "2025-11-10T14:30:00",
                        "notify_on_sale": True,
                        "notify_on_restock": False,
                        "priority": "high",
                        "notes": "Buy this for birthday gift"
                    }
                ],
                "total_items": 1
            }
        }


class WishlistMoveToCart(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1)

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345",
                "quantity": 1
            }
        }
