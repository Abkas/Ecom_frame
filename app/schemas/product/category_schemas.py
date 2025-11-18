from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str = Field(description="Category name like Electronics, Clothing")
    slug: str = Field(description="URL-friendly version: electronics, clothing")
    description: Optional[str] = None
    parent_category: Optional[str] = Field(default=None, description="Parent category ID for subcategories, None for main categories")
    image_url: Optional[str] = None
    is_active: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Electronics",
                "slug": "electronics",
                "description": "Electronic devices and accessories",
                "parent_category": None,
                "image_url": "https://example.com/electronics.jpg",
                "is_active": True
            }
        }


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Consumer Electronics",
                "description": "Updated description for electronics category"
            }
        }


class CategoryResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    slug: str
    description: Optional[str] = None
    parent_category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "64a1b2c3d4e5f6789012345",
                "name": "Electronics",
                "slug": "electronics",
                "description": "Electronic devices and accessories",
                "parent_category": None,
                "image_url": "https://example.com/electronics.jpg",
                "is_active": True,
                "created_at": "2025-11-15T10:30:00"
            }
        }

class CategoryListItem(BaseModel):
    id: str = Field(alias="_id")
    name: str
    slug: str
    parent_category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool


class CategoryToggleActive(BaseModel):
    is_active: bool

