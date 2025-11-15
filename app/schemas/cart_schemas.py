from pydantic import BaseModel, Field
from typing import List


class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = Field(ge=1, description="Quantity to add")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345",
                "quantity": 2
            }
        }

class CartItemUpdate(BaseModel):
    product_id: str
    quantity: int = Field(ge=1, description="New quantity")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345",
                "quantity": 5
            }
        }

class CartItemRemove(BaseModel):
    product_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345"
            }
        }


class CartItemResponse(BaseModel):
    product_id: str
    product_name: str  # Fetched from product collection
    quantity: int
    price: float
    subtotal: float  # price * quantity

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64a1b2c3d4e5f6789012345",
                "product_name": "Wireless Mouse",
                "quantity": 2,
                "price": 25.99,
                "subtotal": 51.98
            }
        }


class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_items: int  # Total count of items
    total_price: float  # Sum of all subtotals

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "product_id": "64a1b2c3d4e5f6789012345",
                        "product_name": "Wireless Mouse",
                        "quantity": 2,
                        "price": 25.99,
                        "subtotal": 51.98
                    }
                ],
                "total_items": 2,
                "total_price": 51.98
            }
        }
