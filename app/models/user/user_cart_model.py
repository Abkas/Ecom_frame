from pydantic import BaseModel ,Field
from typing import Optional , List 
from datetime import datetime

class CartItem(BaseModel):
    product_id : str = Field(description = 'Id of the product')
    quantity : int = Field(ge = 1 , description = 'Quantity in cart')
    price : float = Field(ge=0 , description = 'Price when added to cart')