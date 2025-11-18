from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5, description="Star rating: 1 to 5")
    title: Optional[str] = Field(default=None, max_length=100, description="Optional review title")
    comment: str = Field(max_length=2000, description="Review text")
    image_urls: List[str] = Field(default=[], description="Optional image URLs uploaded by user")

    class Config:
        json_schema_extra = {
            "example": {
                "rating": 5,
                "title": "Excellent product!",
                "comment": "This product exceeded my expectations. Great quality and fast delivery.",
                "image_urls": ["https://example.com/review-photo1.jpg"]
            }
        }


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    title: Optional[str] = Field(default=None, max_length=100)
    comment: Optional[str] = Field(default=None, max_length=2000)
    image_urls: Optional[List[str]] = None
    class Config:
        json_schema_extra = {
            "example": {
                "rating": 4,
                "comment": "Updated my review after using it for a month. Still great!"
            }
        }


class ReviewResponse(BaseModel):
    id: str = Field(alias="_id")
    product_id: str
    user_id: str
    username: str
    rating: int
    title: Optional[str] = None
    comment: str
    is_verified_purchase: bool
    helpful_count: int
    image_urls: List[str]
    is_approved: bool
    created_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "64a1b2c3d4e5f6789012345",
                "product_id": "prod123",
                "user_id": "user456",
                "username": "john_doe",
                "rating": 5,
                "title": "Excellent product!",
                "comment": "This product exceeded my expectations.",
                "is_verified_purchase": True,
                "helpful_count": 12,
                "image_urls": ["https://example.com/review1.jpg"],
                "is_approved": True,
                "created_at": "2025-11-15T10:30:00"
            }
        }


class ReviewListItem(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    username: str
    rating: int
    title: Optional[str] = None
    comment: str
    is_verified_purchase: bool
    helpful_count: int
    created_at: datetime

    class Config:
        populate_by_name = True


class ReviewApprovalUpdate(BaseModel):
    is_approved: bool
    class Config:
        json_schema_extra = {
            "example": {
                "is_approved": False
            }
        }


class ReviewHelpfulUpdate(BaseModel):
    
    action: str = Field(description="'add' to mark helpful, 'remove' to undo")

    class Config:
        json_schema_extra = {
            "example": {
                "action": "add"
            }
        }
