from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user.address_schemas import AddressCreate, AddressResponse, AddressUpdate 
from ecom_backend_framework.app.services.user.address_service import AddressService
from app.core.security import get_current_user  # For authentication

router = APIRouter(
    prefix = '/users/me',
    tags = ['Users-address']
)

@router.get('/addresses', response_model=list[AddressResponse])
async def get_user_addresses(current_user: dict = Depends(get_current_user)):
    result = await AddressService.get_addresses(current_user['user_id']) 
    return result


@router.post('/addresses', response_model=AddressResponse)
async def add_user_address(
    address_data: AddressCreate,
    current_user: dict = Depends(get_current_user)
):
    result = await AddressService.add_address(current_user['user_id'], address_data)
    return result


@router.put('/addresses/{index}', response_model=AddressResponse)
async def update_user_address(
    index: int,
    address_update: AddressUpdate,
    current_user: dict = Depends(get_current_user)
):
    result = await AddressService.update_address(current_user['user_id'], index, address_update)
    return result


@router.delete('/addresses/{index}')
async def delete_user_address(
    index: int,
    current_user: dict = Depends(get_current_user)
):
    await AddressService.delete_address(current_user['user_id'], index)
    return None
    

@router.put('/addresses/{index}/set-default', response_model=list[AddressResponse])
async def set_default_address(
    index: int,
    current_user: dict = Depends(get_current_user)
):
    result = await AddressService.set_default_address(current_user['user_id'], index)
    return result