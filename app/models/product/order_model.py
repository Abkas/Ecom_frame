from pydantic import BaseModel , Field
from typing import Optional , List
from datetime import datetime

class OrderItem(BaseModel) :
    product_id : str
    product_name: str
    quantity: int = Field(ge=1)
    price: float = Field (ge= 0)

class Order(BaseModel):
    id:Optional[str] = Field(default= None , alias ='_id')
    user_id : str = Field(description = "who placed the order")

    items: List[OrderItem]  = Field(description= "products in the order")

    subtotal : float = Field(ge= 0)
    shipping_cost: float = Field(ge= 0)
    total: float = Field(ge=0)

    shipping_address: dict

    order_status : str = Field(default = 'pending', description= "pending, processing , shipped, delivere, cancelled")
    payment_status: str = Field(default='unpaid', description='paid, unpaid , refunded')

    created_at: datetime = Field(default_factory = datetime.now)