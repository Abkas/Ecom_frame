from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CouponCreate(BaseModel):
    code: str = Field(description="Coupon code like SAVE25, NEWYEAR2025")

    discount_type: str = Field(description="'percentage' or 'fixed'")
    discount_value: float = Field(ge=0, description="20 for 20% off or 100 for Rs.100 off")

    min_order_value: Optional[float] = Field(default=None, description="Minimum cart value to apply")
    max_discount: Optional[float] = Field(default=None, description="Max discount for percentage coupons")
    
    usage_limit: Optional[int] = Field(default=None, description="Total usage limit, None = unlimited")
    usage_per_user: int = Field(default=1, description="How many times per user")
    
    valid_from: datetime
    valid_until: datetime
    
    applicable_categories: List[str] = Field(default=[], description="Empty = all categories")
    applicable_products: List[str] = Field(default=[], description="Empty = all products")
    
    is_active: bool = True
    
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": "SAVE25",
                "discount_type": "percentage",
                "discount_value": 25,
                "min_order_value": 1000,
                "max_discount": 500,
                "usage_limit": 100,
                "usage_per_user": 1,
                "valid_from": "2025-11-15T00:00:00",
                "valid_until": "2025-12-31T23:59:59",
                "applicable_categories": [],
                "applicable_products": [],
                "is_active": True,
                "description": "25% off on all products"
            }
        }


class CouponUpdate(BaseModel):
    code: Optional[str] = None

    discount_type: Optional[str] = None
    discount_value: Optional[float] = None

    min_order_value: Optional[float] = None
    max_discount: Optional[float] = None

    usage_limit: Optional[int] = None
    usage_per_user: Optional[int] = None

    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    applicable_categories: Optional[List[str]] = None
    applicable_products: Optional[List[str]] = None

    is_active: Optional[bool] = None

    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "valid_until": "2026-01-31T23:59:59",
                "usage_limit": 200
            }
        }


class CouponValidate(BaseModel):
    coupon_code: str
    cart_total: float = Field(ge=0, description="Total cart value before discount")
    user_id: Optional[str] = Field(default=None, description="User ID for per-user usage validation")

    class Config:
        json_schema_extra = {
            "example": {
                "coupon_code": "SAVE25",
                "cart_total": 1500.00,
                "user_id": "user123"
            }
        }


class CouponValidateResponse(BaseModel):
    is_valid: bool
    message: str  # Success or error message
    discount_amount: float = Field(default=0.0)
    final_total: float = Field(default=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "is_valid": True,
                "message": "Coupon applied successfully",
                "discount_amount": 375.00,
                "final_total": 1125.00
            }
        }


class CouponResponse(BaseModel):
    id: str = Field(alias="_id")
    code: str
    discount_type: str
    discount_value: float
    min_order_value: Optional[float] = None
    max_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    used_count: int
    usage_per_user: int
    valid_from: datetime
    valid_until: datetime
    applicable_categories: List[str]
    applicable_products: List[str]
    is_active: bool
    description: Optional[str] = None
    created_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "64a1b2c3d4e5f6789012345",
                "code": "SAVE25",
                "discount_type": "percentage",
                "discount_value": 25,
                "min_order_value": 1000,
                "max_discount": 500,
                "usage_limit": 100,
                "used_count": 45,
                "usage_per_user": 1,
                "valid_from": "2025-11-15T00:00:00",
                "valid_until": "2025-12-31T23:59:59",
                "applicable_categories": [],
                "applicable_products": [],
                "is_active": True,
                "description": "25% off on all products",
                "created_at": "2025-11-01T10:00:00"
            }
        }


class CouponListItem(BaseModel):
    id: str = Field(alias="_id")
    code: str
    discount_type: str
    discount_value: float
    used_count: int
    usage_limit: Optional[int] = None
    valid_until: datetime
    is_active: bool

    class Config:
        populate_by_name = True
