from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user.user_schema import UserCreate, UserLogin, UserResponse, UserUpdate
from ecom_backend_framework.app.services.user.user_service import register,login,get_user_by_id,update_user, delete_user
from app.core.security import get_current_user  # For authenticatio

router = APIRouter(
    prefix ='/users',
    tags= ['Users']
)

@router.post("/register")
async def register_user(user_credentials: UserCreate):
    result = await register(user_credentials)
    return result

@router.post("/login")
async def login_user(user_credentials: UserLogin):
    result = await login(user_credentials)
    return result

@router.post('/logout')
async def logout_user():
    return {"message": "Logged out successfully"}


# Profile Management Routes

@router.get('/me', response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    result = await get_user_by_id(current_user['user_id'])
    return result


@router.put('/me', response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    result = await update_user(current_user['user_id'], user_update)
    return result


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(current_user: dict = Depends(get_current_user)):
    await delete_user(current_user['user_id'])
    return None 