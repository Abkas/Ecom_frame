from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user.address_schemas import AddressCreate, AddressResponse, AddressUpdate 
from ecom_backend_framework.app.services.user.address_service import add_address, get_address, update_address, delete_address, set_default_address
from app.core.security import get_current_user  # For authentication

router = APIRouter(
    prefix = '/users/me',
    tags = ['Users-address']
)

@router.get('/addresses', response_model=list[AddressResponse])
async def get_user_addresses(current_user: dict = Depends(get_current_user)):
    return get_address(current_user['user_id'])

@router.post('/addresses', response_model=AddressResponse)
async def add_user_address(
    address_data: AddressCreate,
    current_user: dict = Depends(get_current_user)
):
    return add_address(current_user['user_id'], address_data)

@router.put('/addresses/{address_id}', response_model=AddressResponse)
async def update_user_address(
    address_id: str,
    address_update: AddressUpdate,
    current_user: dict = Depends(get_current_user)
):
    return update_address(address_id, address_update)

@router.delete('/addresses/{address_id}')
async def delete_user_address(
    address_id: str,
    current_user: dict = Depends(get_current_user)
):
    return delete_address(address_id)

@router.put('/addresses/{address_id}/default')
async def set_default_user_address(
    address_id: str,
    current_user: dict = Depends(get_current_user)
):
    success = set_default_address(current_user['user_id'], address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found or not updated")
    return {"message": "Default address set successfully"}