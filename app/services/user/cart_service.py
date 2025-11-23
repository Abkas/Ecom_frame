from core.database import db
from bson.objectid import ObjectId

def get_cart(user_id):
    cart = db['carts'].find_one({'user_id': user_id})
    if cart:
        cart['_id'] = str(cart['_id'])
        cart["total_price"] = calculate_cart_total(cart)
    return cart

def add_to_cart(user_id , cart_item):
    product_id = cart_item.product_id
    quantity = cart_item.quantity
    if not validate_stock(product_id, quantity):
        raise Exception("Not enough stock")
    
    cart = db['carts'].find_one({'user_id' : user_id})
    if cart:
        for item in cart['items']:
            if item['product_id'] == product_id:
                item['quantity'] == quantity
                break
        else:
            cart['items'].append({'product_id': product_id, 'quantity': quantity})
        db["carts"].update_one({"_id": cart["_id"]}, {"$set": {"items": cart["items"]}})
    else:
        db['carts'].insert_one({
            'user_id': user_id,
            'items': [{'product_id': product_id, 'quantity': quantity}]
        })

    return get_cart(user_id)

def update_cart(user_id, cart_update):

    items = [{"product_id": item.product_id, "quantity": item.quantity} for item in cart_update.items]
    db["carts"].update_one({"user_id": user_id}, {"$set": {"items": items}})
    return get_cart(user_id)

def remove_from_cart(user_id, product_id):
    cart = db["carts"].find_one({"user_id": user_id})
    if cart:
        new_items = []
        for item in cart["items"]:
            if item["product_id"] != product_id:
                new_items.append(item)
        db["carts"].update_one({"_id": cart["_id"]}, {"$set": {"items": new_items}})
    return get_cart(user_id)

def clear_cart(user_id):
    db["carts"].update_one({"user_id": user_id}, {"$set": {"items": []}})
    return get_cart(user_id)


def calculate_cart_total(cart):
    total = 0
    for item in cart["items"]:
        product = db["products"].find_one({"_id": ObjectId(item["product_id"])})
        if product:
            total += product["price"] * item["quantity"]
    return total

def validate_stock(product_id, quantity):
    product = db["products"].find_one({"_id": ObjectId(product_id)})
    if not product or product["stock"] < quantity:
        return False
    return True