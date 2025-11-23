from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user.cart_schemas import CartItemResponse, CartItemRemove, CartItemAdd, CartItemUpdate, CartResponse
from ecom_backend_framework.app.services.user.cart_service import clear_cart , get_cart , add_to_cart , update_cart ,remove_from_cart
from app.core.security import get_current_user  # For authentication

router = APIRouter(
    prefix ='/users/me',
    tags= ['Users-cart']
)

@router.get("/cart", response_model=CartResponse)
async def get_user_cart(current_user: dict = Depends(get_current_user)):
    result = await get_cart(current_user['user_id'])
    return result 

@router.post("/cart", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    cart_item: CartItemAdd,
    current_user: dict = Depends(get_current_user),
):
    result = await add_to_cart(current_user['user_id'], cart_item)
    return result

@router.put("/cart", response_model=CartResponse)
async def update_cart_item(
    cart_update: CartItemUpdate,
    current_user: dict = Depends(get_current_user)
):
    result = await update_cart(current_user['user_id'], cart_update)
    return result

@router.delete("/cart/{product_id}")
async def remove_from_cart(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    await remove_from_cart(current_user['user_id'],product_id)
    return None

@router.delete("/cart")
async def clear_cart(
    current_user : dict = Depends(get_current_user)
):
    await clear_cart(current_user)
    return None