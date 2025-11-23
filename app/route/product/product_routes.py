from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from app.schemas.product.product_schemas import (CreateProduct, ProductDetailUpdate, ProductPriceUpdate, ProductStockUpdate, ChangeAvailabilityProduct, ProductResponse)
from ecom_backend_framework.app.services.product.product_service import change_availability,get_product_by_id, create_product, delete_product, update_product , update_product_price ,update_product_stock ,get_all_products
from app.core.security import get_admin_user

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

# Public Routes - Product Browsing

@router.get('/', response_model=list[ProductResponse])
async def get_all_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_available: Optional[bool] = True,
    skip: int = 0,
    limit: int = 50
):
    result = await get_all_products(
        category=category,
        search=search,
        min_price=min_price,
        max_price=max_price,
        is_available=is_available,
        skip=skip,
        limit=limit
    )
    return result


@router.get('/{product_id}', response_model=ProductResponse)
async def get_product_by_id(product_id: str):
    result = await get_product_by_id(product_id)
    return result


# Admin Routes - Product Management

@router.post('/', response_model=ProductResponse)
async def create_product(
    product: CreateProduct,
    admin_user: dict = Depends(get_admin_user)
):
    result = await create_product(product)
    return result


@router.put('/{product_id}/details', response_model=ProductResponse)
async def update_product_details(
    product_id: str,
    product_update: ProductDetailUpdate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await update_product(product_id, product_update)
    return result


@router.put('/{product_id}/price', response_model=ProductResponse)
async def update_product_price(
    product_id: str,
    price_update: ProductPriceUpdate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await update_product_price(product_id, price_update)
    return result


@router.put('/{product_id}/stock', response_model=ProductResponse)
async def update_product_stock(
    product_id: str,
    stock_update: ProductStockUpdate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await update_product_stock(product_id, stock_update)
    return result


@router.patch('/{product_id}/availability', response_model=ProductResponse)
async def toggle_product_availability(
    product_id: str,
    availability: ChangeAvailabilityProduct,
    admin_user: dict = Depends(get_admin_user)
):

    result = await change_availability(product_id, availability.is_available)
    return result


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    await delete_product(product_id)
    return None
