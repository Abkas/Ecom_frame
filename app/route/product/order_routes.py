from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.product.order_schemas import OrderCreate, OrderItemSchema, OrderListItem, OrderPaymentUpdate, OrderResponse, OrderStatusUpdate
from ecom_backend_framework.app.services.product.order_service import get_order_by_id,cancel_order,create_order,update_order_status,get_all_orders,get_user_orders
from app.core.security import get_current_user, get_admin_user


router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


# User Routes - Order Management

@router.post('/', response_model=OrderResponse)
async def place_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_user)
):
    result = await create_order(current_user['user_id'], order_data)
    return result

@router.get('/me', response_model=list[OrderListItem])
async def get_my_orders(current_user: dict = Depends(get_current_user)):
    result = await get_user_orders(current_user['user_id'])
    return result


@router.get('/{order_id}', response_model=OrderResponse)
async def get_order_by_id(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    result = await get_order_by_id(order_id, current_user['user_id'])
    return result


@router.post('/{order_id}/cancel', response_model=OrderResponse)
async def cancel_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    result = await cancel_order(order_id, current_user['user_id'])
    return result


# Admin Routes - Order Management

@router.get('/', response_model=list[OrderListItem])
async def get_all_orders(
    admin_user: dict = Depends(get_admin_user),
    status_filter: str = None,
    limit: int = 50
):
    result = await get_all_orders(status_filter, limit)
    return result


@router.patch('/{order_id}/status', response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await update_order_status(order_id, status_update.status)
    return result


@router.patch('/{order_id}/payment', response_model=OrderResponse)
async def update_payment_status(
    order_id: str,
    payment_update: OrderPaymentUpdate,
    admin_user: dict = Depends(get_admin_user)
):
    result = await update_payment_status(order_id, payment_update.payment_status)
    return result



