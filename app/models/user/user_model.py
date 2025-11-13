from pydantic import BaseModel, Field, EmailStr
from typing import Optional , List
from datetime import datetime
from ecom_backend_framework.app.models.user.user_address_model import Address
from ecom_backend_framework.app.models.user.user_cart_model import CartItem

class User(BaseModel):
    id: Optional[str] =Field(default = None , alias= '_id')
    password: str = Field(min_length = 5)
    email: EmailStr = Field(...)
    username: str = Field(min_length = 3,  max_length = 10)
    firstname : str = Field(description = "The users first name")
    lastname : str = Field(description = "The users last name")

    phone:Optional[str] =Field(default= None)
    profile_image :Optional[str] = Field(default = None, description='User image')
    addresses : List[Address] = Field(default = [], description="Users saved addresses")

    Cart : List[CartItem] = Field(default = [] , description = 'Shopping Cart')

    order_history: List[str] = Field(default=[], description="List of order IDs")
    wishlist: List[str] = Field(default=[], description="Product IDs user wants to buy later")
    
    is_verified :bool = Field(default = False, description = 'Email Verified')
    is_active: bool = Field(default=True, description="Account status")
    is_admin: bool = Field(default=False)

    created_at :datetime = Field(default_factory = datetime.now)
    last_login: Optional[datetime] = Field(default=None)