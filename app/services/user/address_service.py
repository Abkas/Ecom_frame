
from core.database import db
from bson.objectid import ObjectId

def get_address(user_id):
    addresses = list(db['addressses'].find({'user_id':user_id}))
    for addr in addresses:
        addr['_id'] = str(addr['_id'])
    return addresses

def add_address(user_id, address_data):
    address_data['user_id'] = user_id
    result = db['addresses'].insert_one(address_data)
    return str(result.inserted_id)

def update_address(address_id, user_id, update_data):
    result = db["addresses"].update_one(
        {"_id": ObjectId(address_id), "user_id": user_id},
        {"$set": update_data.dict(exclude_unset=True)}
    )
    if result.modified_count:
        return get_address_by_id(address_id, user_id)
    return None

def get_address_by_id(address_id, user_id):
    address = db["addresses"].find_one({"_id": ObjectId(address_id), "user_id": user_id})
    if address:
        address["_id"] = str(address["_id"])
    return address

def delete_address(address_id, user_id):
    result = db["addresses"].delete_one({"_id": ObjectId(address_id), "user_id": user_id})
    return result.deleted_count > 0

def set_default_address(user_id, address_id):
    # Unset previous default
    db["addresses"].update_many({"user_id": user_id, "is_default": True}, {"$set": {"is_default": False}})
    # Set new default
    result = db["addresses"].update_one({"_id": ObjectId(address_id), "user_id": user_id}, {"$set": {"is_default": True}})
    return result.modified_count > 0