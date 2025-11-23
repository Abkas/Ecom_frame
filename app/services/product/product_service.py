from core.database import db
from bson.objectid import ObjectId

def get_all_products(category=None, search=None, min_price=None, max_price=None, is_available=True, skip=0, limit=50):
    query = {}
    if category:
        query["category"] = category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    if min_price is not None or max_price is not None:
        price_query = {}
        if min_price is not None:
            price_query["$gte"] = min_price
        if max_price is not None:
            price_query["$lte"] = max_price
        query["price"] = price_query
    if is_available is not None:
        query["is_available"] = is_available
    products = list(db["products"].find(query).skip(skip).limit(limit))
    for product in products:
        product["_id"] = str(product["_id"])
    return products

def get_product_by_id(product_id):
    product = db["products"].find_one({"_id": ObjectId(product_id)})
    if product:
        product["_id"] = str(product["_id"])
    return product

def create_product(product_data):
    result = db["products"].insert_one(product_data.dict())
    return get_product_by_id(str(result.inserted_id))

def update_product(product_id, product_update):
    result = db["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product_update.dict(exclude_unset=True)}
    )
    if result.modified_count:
        return get_product_by_id(product_id)
    return None

def update_product_price(product_id, price_update):
    result = db["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"price": price_update.price}}
    )
    if result.modified_count:
        return get_product_by_id(product_id)
    return None

def update_product_stock(product_id, stock_update):
    result = db["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"stock": stock_update.stock}}
    )
    if result.modified_count:
        return get_product_by_id(product_id)
    return None

def change_availability(product_id, is_available):
    result = db["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"is_available": is_available}}
    )
    if result.modified_count:
        return get_product_by_id(product_id)
    return None

def delete_product(product_id):
    result = db["products"].delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0



