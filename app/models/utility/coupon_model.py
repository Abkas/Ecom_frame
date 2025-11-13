from pydantic import BaseModel , Field
from typing import List, Optional
from datetime import datetime

class Coupon(BaseModel):
    id: Optional[str] = Field(default = None , alias ="_id")
    code: str = Field(description ='Coupon code like SAVE25')

    discount_type : str = Field(description = 'percentage or fixed')
    discount_value: float = Field(ge=0, description="20 for 20% off or 100 for Rs.100 off")
    
    # Conditions
    min_order_value: Optional[float] = Field(default=None, description="Minimum cart value to apply coupon")
    max_discount: Optional[float] = Field(default=None, description="Maximum discount amount (for percentage)")
    
    # Usage limits
    usage_limit: Optional[int] = Field(default=None, description="Total number of times coupon can be used")
    used_count: int = Field(default=0, description="How many times coupon has been used")
    usage_per_user: int = Field(default=1, description="How many times each user can use it")
    
    # Validity period
    valid_from: datetime = Field(description="Coupon valid from this date")
    valid_until: datetime = Field(description="Coupon expires after this date")
    
    # Restrictions (optional)
    applicable_categories: List[str] = Field(default=[], description="Category IDs - empty means all categories")
    applicable_products: List[str] = Field(default=[], description="Product IDs - empty means all products")
    
    # Status
    is_active: bool = Field(default=True, description="Is coupon active?")
    
    # Metadata
    description: Optional[str] = Field(default=None, description="Description for admin")
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = Field(default=None, description="Admin user ID who created it")