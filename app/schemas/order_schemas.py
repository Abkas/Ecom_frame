from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
class OrderItemSchema(BaseModel):
    product_id: str 
    product_name: str 
    quantity: int = Field(ge=1)
    price: float = Field(ge=0)
class OrderCreate(BaseModel):
    address_index: int = Field(ge=0, description="Which saved address to use (0 = first address)")
    payment_method: str = Field(description="Payment method: cod, esewa, khalti, bank_transfer")
    
    coupon_code: Optional[str] = Field(default=None, description="Coupon code if any")

class OrderResponse(BaseModel):
    id: str 
    user_id: str

    items: List[OrderItemSchema] = Field(description="List of products ordered")
    
    subtotal: float = Field(ge=0)
    shipping_cost: float = Field(ge=0)
    total: float = Field(ge=0)

    shipping_address: dict 
    
    status: str = Field(description="Order status: pending, processing, shipped, delivered, cancelled")
    payment_status: str = Field(description="Payment status: unpaid, paid, failed, refunded")
    
    created_at: datetime = Field(description="When order was placed")
    
class OrderStatusUpdate(BaseModel):
    status: str = Field(
        description="New order status",
        json_schema_extra={
            "enum": ["pending", "processing", "shipped", "delivered", "cancelled"]
        }
    )
class OrderPaymentUpdate(BaseModel):
    payment_status: str = Field(
        description="New payment status",
        json_schema_extra={
            "enum": ["unpaid", "paid", "failed", "refunded"]
        }
    )
class OrderListItem(BaseModel):
    id: str
    total: float

    status: str
    payment_status: str

    created_at: datetime
    item_count: int = Field(description="How many different products in order")
