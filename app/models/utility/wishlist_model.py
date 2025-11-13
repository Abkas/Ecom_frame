from pydantic import BaseModel , Field
from typing import Optional , List
from datetime import datetime

class WishlistItem(BaseModel):
    product_id: str = Field(description = 'Product id')
    added_at: datetime = Field(default_factory=datetime.now, description="When added to wishlist")

    notify_on_sale: bool = Field(default=False, description="Notify when product goes on sale")
    notify_on_restock: bool = Field(default=False, description="Notify when back in stock")
    priority: str = Field(default="normal", description="low, normal, high - how much they want it")
    notes: Optional[str] = Field(default=None, max_length=200, description="User's personal note")


class Wishlist(BaseModel):
    id: Optional[str] = Field(default=None, alias='_id')
    user_id: str = Field(description="Which user's wishlist")
    items: List[WishlistItem] = Field(default=[], description="Wishlist items")
    updated_at: datetime = Field(default_factory=datetime.now)