from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.utility.wishlist_schemas import WishlistItemAdd, WishlistItemRemove, WishlistItemResponse, WishlistItemUpdate, WishlistMoveToCart, WishlistResponse
from ecom_backend_framework.app.services.utility.wishlist_service import add_item,update_item,delete_item,get_wishlist
from app.core.security import get_current_user  # For authentication

router = APIRouter(
    prefix ='/users/me',
    tags= ['Users-wishlist']
)

@router.get('/wishlist', response_model=WishlistResponse)
async def get_user_wishlist(current_user: dict = Depends(get_current_user)):
    result = await get_wishlist(current_user['user_id'])
    return result

@router.post('/wishlist', response_model=WishlistResponse)
async def add_item_to_wishlist(
    wishlist_item: WishlistItemAdd,
    current_user: dict = Depends(get_current_user)
):
    result = await add_item(current_user['user_id'], wishlist_item)
    return result

@router.put('/wishlist/{product_id}', response_model=WishlistResponse)
async def update_wishlist_item(
    product_id: str,
    wishlist_update: WishlistItemUpdate,
    current_user: dict = Depends(get_current_user)
):
    result = await update_item(current_user['user_id'], product_id, wishlist_update)
    return result

@router.delete('/wishlist/{product_id}')
async def delete_item_from_wishlist(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    await delete_item(current_user['user_id'], product_id)
    return None

@router.post('/wishlist/{product_id}/move-to-cart')
async def move_wishlist_to_cart(
    product_id: str,
    move_data: WishlistMoveToCart,
    current_user: dict = Depends(get_current_user)
):
    result = await move_to_cart(current_user['user_id'], product_id, move_data)
    return result