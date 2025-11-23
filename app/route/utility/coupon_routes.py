from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.utility.coupon_schemas import CouponCreate, CouponListItem, CouponResponse, CouponUpdate, CouponValidate, CouponValidateResponse
from ecom_backend_framework.app.services.utility.coupon_service import create_coupon,get_coupon_by_id,apply_coupon_to_cart,delete_coupon,toggle_coupon_activity,update_coupon,get_all_coupons,validate_coupon,get_active_coupons.core.security import get_current_user, get_admin_user
from app.core.security import get_current_user, get_admin_user

router = APIRouter(
    prefix='/coupons',
    tags=['Coupons']
)


# Admin Routes - Coupon Management

@router.post('/', response_model=CouponResponse)
async def create_coupon(
    coupon: CouponCreate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await create_coupon(coupon, admin_user['user_id'])
    return result


@router.get('/', response_model=list[CouponListItem])
async def get_all_coupons(admin_user: dict = Depends(get_admin_user)):
    result = await get_all_coupons()
    return result


@router.get('/{coupon_id}', response_model=CouponResponse)
async def get_coupon_by_id(
    coupon_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    result = await get_coupon_by_id(coupon_id)
    return result


@router.put('/{coupon_id}', response_model=CouponResponse)
async def update_coupon(
    coupon_id: str,
    coupon_update: CouponUpdate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await update_coupon(coupon_id, coupon_update)
    return result


@router.delete('/{coupon_id}')
async def delete_coupon(
    coupon_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    await delete_coupon(coupon_id)
    return None


@router.patch('/{coupon_id}/toggle', response_model=CouponResponse)
async def toggle_coupon_activity_route(
    coupon_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    result = await toggle_coupon_activity(coupon_id)
    if not result:
        raise HTTPException(status_code=404, detail="Coupon not found or not updated")
    return result


# User Routes - Apply Coupons

@router.post('/validate', response_model=CouponValidateResponse)
async def validate_coupon(
    validation_data: CouponValidate,
    current_user: dict = Depends(get_current_user)
):
    result = validate_coupon(
        validation_data.coupon_code,
        validation_data.cart_total,
        current_user['user_id']
    )
    return result


@router.get('/active', response_model=list[CouponListItem])
async def get_active_coupons():
    result = await get_active_coupons()
    return result