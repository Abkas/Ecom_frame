from pydantic import BaseModel , Field
from typing import Optional , list
from datetime import datetime

class Payment(BaseModel):
    id: Optional[str] = Field(default = None , alias = "_id")
    order_id: str = Field(description= "which order this payment is for")
    user_id: str = Field(description = "who made the payment")

    amount: float = Field(ge=0)
    currency: str = Field(default = "NPR")

    payment_method : str = Field(description = 'esewa, khalti , banking, qr')

    # External payment gateway info
    transaction_id: Optional[str] = Field(default=None, description="Transaction ID from payment gateway")
    gateway_response: Optional[dict] = Field(default=None, description="Response from payment gateway")


    payment_status: str = Field(
        default= 'pending',
        description = 'pending, processing, completed, failed'
    )



    created_at: datetime = Field(default_factory = datetime.now ,description ="when payment was initiated")
    completed_at : Optional[datetime] = Field(default = None, description = 'when payment was completed')


    refund_amount: Optional[float] = Field(default=None, ge=0)
    refund_reason: Optional[str] = Field(default=None)
    refunded_at: Optional[datetime] = Field(default=None)
