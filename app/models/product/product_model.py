from pydantic import BaseModel, Field
from typing import Optional ,List
from datetime import datetime

class Product(BaseModel):
    id : Optional[str] = Field(default = None, alias = '_id')
    name : str = Field(description = 'Name of the product')
    description : str = Field(description = 'Description of the product')

    original_price: float = Field(ge=0, description="Original/MRP price")
    discount_percentage: Optional[float] = Field(default=None, ge=0, le=100, description="Discount %")
    price: float = Field(ge=0, description="Current selling price (after discount)")
    currency : Optional[str] = Field(default= "NPR")
 
    stock_quantity : Optional[int] = Field(default=0)
    is_available : bool = Field(default = True)

    category : str = Field(description = "Product category", default = 'Basic')
    subcategory : Optional[str] = Field(default = None)
    tags : List[str] = Field(default = [])

    image_urls :List[str] = Field(default= [])

    ratings : Optional[int] =Field(default = 0.0, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    comments : List[str] = Field(default = [])

    created_at: datetime = Field(default_factory=datetime.now)

    is_active: bool = Field(default = True)
