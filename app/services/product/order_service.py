from core.database import db
from bson.objectid import ObjectId

def create_order(user_id, order_data):
	order_dict = order_data.dict()
	order_dict["user_id"] = user_id
	order_dict["status"] = "pending"
	result = db["orders"].insert_one(order_dict)
	return get_order_by_id(str(result.inserted_id), user_id)

def get_user_orders(user_id):
	orders = list(db["orders"].find({"user_id": user_id}))
	for order in orders:
		order["_id"] = str(order["_id"])
	return orders

def get_order_by_id(order_id, user_id):
	order = db["orders"].find_one({"_id": ObjectId(order_id), "user_id": user_id})
	if order:
		order["_id"] = str(order["_id"])
	return order

def cancel_order(order_id, user_id):
	result = db["orders"].update_one(
		{"_id": ObjectId(order_id), "user_id": user_id},
		{"$set": {"status": "cancelled"}}
	)
	if result.modified_count:
		return get_order_by_id(order_id, user_id)
	return None

def get_all_orders(status_filter=None, limit=50):
	query = {}
	if status_filter:
		query["status"] = status_filter
	orders = list(db["orders"].find(query).limit(limit))
	for order in orders:
		order["_id"] = str(order["_id"])
	return orders

def update_order_status(order_id, status):
	result = db["orders"].update_one(
		{"_id": ObjectId(order_id)},
		{"$set": {"status": status}}
	)
	if result.modified_count:
		return db["orders"].find_one({"_id": ObjectId(order_id)})
	return None

def update_payment_status(order_id, payment_status):
	result = db["orders"].update_one(
		{"_id": ObjectId(order_id)},
		{"$set": {"payment_status": payment_status}}
	)
	if result.modified_count:
		return db["orders"].find_one({"_id": ObjectId(order_id)})
	return None
