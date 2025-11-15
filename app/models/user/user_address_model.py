from pydantic import BaseModel, Field
from typing import Optional


class Address(BaseModel):
    full_name : str 
    phone_number : str

    address_type : str = Field(default = 'Home')
    is_default : bool = Field(default = False , description = "Quick checkout uses default")


    country : str = Field(default = 'Nepal')
    province : str = Field(...)
    district : str = Field(...)
    city : str = Field(...)
    tole : Optional[str] = Field(default = None)
    landmark : Optional[str] = Field(default = None , description="eg: Near Sajha Park")