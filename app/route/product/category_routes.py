from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.product.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryListItem, CategoryToggleActive
from ecom_backend_framework.app.services.product.category_service import CategoryService
from app.core.security import get_admin_user


router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)


# Public Routes

@router.get('/', response_model=list[CategoryListItem])
async def get_all_categories():
    result = await CategoryService.get_all_categories()
    return result


@router.get('/{category_id}', response_model=CategoryResponse)
async def get_category_by_id(category_id: str):
    result = await CategoryService.get_category_by_id(category_id)
    return result


# Admin Routes

@router.post('/', response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await CategoryService.create_category(category)
    return result


@router.put('/{category_id}', response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category_update: CategoryUpdate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await CategoryService.update_category(category_id, category_update)
    return result


@router.patch('/{category_id}/toggle-active', response_model=CategoryResponse)
async def toggle_category_active(
    category_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    result = await CategoryService.toggle_category_active(category_id)
    return result


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    await CategoryService.delete_category(category_id)
    return None
