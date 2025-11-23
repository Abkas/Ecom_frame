from core.database import db
from bson.objectid import ObjectId
from datetime import datetime

def get_wishlist(user_id):
	wishlist = db["wishlists"].find_one({"user_id": user_id})
	items = wishlist["items"] if wishlist and "items" in wishlist else []
	response_items = []
	for item in items:
		product = db["products"].find_one({"_id": ObjectId(item["product_id"])})
		response_items.append({
			"product_id": item["product_id"],
			"product_name": product["name"] if product else "Unknown",
			"product_price": product["price"] if product else 0.0,
			"product_image": product["images"][0] if product and product.get("images") else None,
			"is_available": product["is_available"] if product else False,
			"added_at": item["added_at"],
			"notify_on_sale": item.get("notify_on_sale", False),
			"notify_on_restock": item.get("notify_on_restock", False),
			"priority": item.get("priority", "normal"),
			"notes": item.get("notes")
		})
	return {
		"items": response_items,
		"total_items": len(response_items)
	}

def add_item(user_id, wishlist_item):
	wishlist = db["wishlists"].find_one({"user_id": user_id})
	item = wishlist_item.dict()
	item["added_at"] = datetime.utcnow()
	if wishlist:
		for existing in wishlist["items"]:
			if existing["product_id"] == item["product_id"]:
				raise Exception("Product already in wishlist")
		db["wishlists"].update_one({"user_id": user_id}, {"$push": {"items": item}})
	else:
		db["wishlists"].insert_one({"user_id": user_id, "items": [item]})
	return get_wishlist(user_id)

def update_item(user_id, product_id, wishlist_update):
	wishlist = db["wishlists"].find_one({"user_id": user_id})
	if not wishlist:
		raise Exception("Wishlist not found")
	updated = False
	for idx, item in enumerate(wishlist["items"]):
		if item["product_id"] == product_id:
			for key, value in wishlist_update.dict(exclude_unset=True).items():
				wishlist["items"][idx][key] = value
			updated = True
	if updated:
		db["wishlists"].update_one({"user_id": user_id}, {"$set": {"items": wishlist["items"]}})
	else:
		raise Exception("Product not found in wishlist")
	return get_wishlist(user_id)

def delete_item(user_id, product_id):
	db["wishlists"].update_one({"user_id": user_id}, {"$pull": {"items": {"product_id": product_id}}})
	return

