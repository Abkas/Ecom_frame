from pydantic import BaseModel , Field
from typing import List , Optional
from datetime import datetime

class Review(BaseModel):
    id: Optional[str] = Field(default=None, alias='_id')
    product_id: str = Field(description="Which product")
    user_id: str = Field(description="Who wrote the review")
    username: str = Field(description="For display")
    
    rating: int = Field(ge=1, le=5, description="1-5 stars")
    title: Optional[str] = Field(default=None, max_length=100)
    comment: str = Field(max_length=2000)
    
    # Verification
    is_verified_purchase: bool = Field(default=False, description="Did they actually buy it?")
    
    # Helpfulness
    helpful_count: int = Field(default=0, description="How many found this helpful")
    
    # Images (optional)
    image_urls: List[str] = Field(default=[], description="User uploaded images")
    
    # Admin moderation
    is_approved: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.now)