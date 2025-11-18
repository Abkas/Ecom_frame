from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.utility.coupon_schemas import CouponCreate, CouponListItem, CouponResponse, CouponUpdate, CouponValidate, CouponValidateResponse
from ecom_backend_framework.app.services.utility.coupon_service import CouponService
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
    result = await CouponService.create_coupon(coupon, admin_user['user_id'])
    return result


@router.get('/', response_model=list[CouponListItem])
async def get_all_coupons(admin_user: dict = Depends(get_admin_user)):
    result = await CouponService.get_all_coupons()
    return result


@router.get('/{coupon_id}', response_model=CouponResponse)
async def get_coupon_by_id(
    coupon_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    result = await CouponService.get_coupon_by_id(coupon_id)
    return result


@router.put('/{coupon_id}', response_model=CouponResponse)
async def update_coupon(
    coupon_id: str,
    coupon_update: CouponUpdate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await CouponService.update_coupon(coupon_id, coupon_update)
    return result


@router.delete('/{coupon_id}')
async def delete_coupon(
    coupon_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    await CouponService.delete_coupon(coupon_id)
    return None


@router.patch('/{coupon_id}/toggle-active', response_model=CouponResponse)
async def toggle_coupon_active(
    coupon_id: str,
    admin_user: dict = Depends(get_admin_user)
):
    result = await CouponService.toggle_active(coupon_id)
    return result


# User Routes - Apply Coupons

@router.post('/validate', response_model=CouponValidateResponse)
async def validate_coupon(
    validation_data: CouponValidate,
    current_user: dict = Depends(get_current_user)
):
    result = await CouponService.validate_coupon(
        validation_data.coupon_code,
        validation_data.cart_total,
        current_user['user_id']
    )
    return result


@router.get('/active', response_model=list[CouponListItem])
async def get_active_coupons():
    result = await CouponService.get_active_coupons()
    return result