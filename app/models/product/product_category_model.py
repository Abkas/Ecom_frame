from pydantic import BaseModel , Field
from typing import List, Optional
from datetime import datetime

class Category(BaseModel):
    id: Optional[str] = Field(default= None, alias= '_id')
    name: str = Field(description = "Category name like Electronics,Clothing")
    slug: str = Field(description="electronics, clothing (URL-friendly)")
    
    description :Optional[str]= Field(default = None)

    parent_category: Optional[str] = Field(default = None, descriptoin ="For Subcategories")

    image_url: Optional[str] = Field(default = None)
    is_active: bool = Field(default = True)

    created_at : datetime = Field(Default_factory = datetime.now)