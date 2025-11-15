from pydantic import BaseModel, Field, EmailStr
from typing import Optional , List
from datetime import datetime

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    firstname :str
    lastname:str
    phone:Optional[str]

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    firstname: str
    lastname: str

    phone: Optional[str]
    profile_image:Optional[str]

    is_verified:Optional[str]
    is_admin:Optional[str]

    created_at : datetime

class UserUpdate(BaseModel):
    username: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    profile_image: Optional[str]

class UserPassowrdChange(BaseModel):
    old_password: str = Field(min_length = 5)
    new_password: str = Field(min_length = 5)
    confirm_password: str = Field(min_length = 5)

class UserPasswordResetRequest(BaseModel):
    email: EmailStr = Field(descripton = 'Email to send reset pw link to')