

from core.database import db
from core.security import hash_password, verify_password, create_access_token
from bson.objectid import ObjectId

def register(user_data):
    user_data['password'] = hash_password(user_data['password'])
    result = db['users'].insert_one(user_data)
    return str(result.inserted_id)

def login(user_data):
    user = db['users'].find_one[{'email'}:user_data['email']]
    if user and verify_password(user_data['password'], user['password']):
        token_data = {"user_id": str(user["_id"]), "email": user["email"]}
        access_token = create_access_token(token_data)
        return{'access_token': access_token, 'user': token_data}
    return None

def get_user_by_id(user_id):
    user = db['users'].find_one({'_id': ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
    return user

def update_user(user_id, update_data):
    result = db['users'].update_one(
        {'_id': ObjectId(user_id)},
        {'$set': update_data.dict(exclude_unset = True)}
        )
    if result.modified_count:
        return get_user_by_id(user_id)
    return None

def delete_user(user_id):
    result = db["users"].delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0