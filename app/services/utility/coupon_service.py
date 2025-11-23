
from core.database import db
from bson.objectid import ObjectId
import datetime

def create_coupon(coupon_data):
	result = db["coupons"].insert_one(coupon_data.dict())
	coupon = coupon_data.dict()
	coupon["_id"] = str(result.inserted_id)
	return coupon

def get_coupon_by_id(coupon_id):
	coupon = db["coupons"].find_one({"code": coupon_id})
	if coupon:
		coupon["_id"] = str(coupon["_id"])
	return coupon

def get_all_coupons(skip=0, limit=50):
	coupons = list(db["coupons"].find().skip(skip).limit(limit))
	for coupon in coupons:
		coupon["_id"] = str(coupon["_id"])
	return coupons

def update_coupon(coupon_id, update_data):
	result = db["coupons"].update_one(
		{"_id": ObjectId(coupon_id)},
		{"$set": update_data.dict(exclude_unset=True)}
	)
	if result.modified_count:
		return get_coupon_by_id(coupon_id)
	return None

def get_coupon_by_id(coupon_id):
	coupon = db["coupons"].find_one({"_id": ObjectId(coupon_id)})
	if coupon:
		coupon["_id"] = str(coupon["_id"])
	return coupon

def delete_coupon(coupon_id):
	result = db["coupons"].delete_one({"_id": ObjectId(coupon_id)})
	return result.deleted_count > 0

def apply_coupon_to_cart(user_id, code, cart_total):
	result = validate_coupon(code, cart_total, user_id)
	if not result["is_valid"]:
		return result  # Contains error message and original total

	# Record coupon usage for user only if valid
	db["coupon_usages"].insert_one({
		"coupon_code": code,
		"user_id": user_id,
		"used_at": datetime.datetime.utcnow()
	})

	return result  # Contains discount_amount, final_total, success message

def toggle_coupon_activity(coupon_id):
    coupon = db["coupons"].find_one({"_id": ObjectId(coupon_id)})
    if not coupon:
        return None
    new_status = not coupon.get("is_active", True)
    result = db["coupons"].update_one(
        {"_id": ObjectId(coupon_id)},
        {"$set": {"is_active": new_status}}
    )
    if result.modified_count:
        return get_coupon_by_id(coupon_id)
    return None


def validate_coupon(code, cart_total, user_id=None):
	coupon = get_coupon_by_id(code)
	now = datetime.datetime.utcnow()
	if not coupon:
		return {
			"is_valid": False,
			"message": "Coupon not found",
			"discount_amount": 0.0,
			"final_total": cart_total
		}
	if not coupon.get("is_active", True):
		return {
			"is_valid": False,
			"message": "Coupon is not active",
			"discount_amount": 0.0,
			"final_total": cart_total
		}
	if now < coupon["valid_from"] or now > coupon["valid_until"]:
		return {
			"is_valid": False,
			"message": "Coupon expired or not yet valid",
			"discount_amount": 0.0,
			"final_total": cart_total
		}
	if coupon.get("min_order_value") and cart_total < coupon["min_order_value"]:
		return {
			"is_valid": False,
			"message": f"Minimum order value is {coupon['min_order_value']}",
			"discount_amount": 0.0,
			"final_total": cart_total
		}
	if coupon.get("usage_limit") is not None and coupon.get("used_count", 0) >= coupon["usage_limit"]:
		return {
			"is_valid": False,
			"message": "Coupon usage limit reached",
			"discount_amount": 0.0,
			"final_total": cart_total
		}
	# Per-user usage (requires user_id)
	if user_id and coupon.get("usage_per_user", 1) > 0:
		user_usage = db["coupon_usages"].count_documents({"coupon_code": code, "user_id": user_id})
		if user_usage >= coupon["usage_per_user"]:
			return {
				"is_valid": False,
				"message": "User usage limit reached",
				"discount_amount": 0.0,
				"final_total": cart_total
			}
	# Calculate discount
	discount = 0.0
	if coupon["discount_type"] == "percentage":
		discount = cart_total * (coupon["discount_value"] / 100)
		if coupon.get("max_discount"):
			discount = min(discount, coupon["max_discount"])
	elif coupon["discount_type"] == "fixed":
		discount = coupon["discount_value"]
	final_total = max(cart_total - discount, 0.0)
	return {
		"is_valid": True,
		"message": "Coupon applied successfully",
		"discount_amount": discount,
		"final_total": final_total
	}

def get_active_coupons(skip=0, limit=50):
	coupons = list(db["coupons"].find({"is_active": True}).skip(skip).limit(limit))
	for coupon in coupons:
		coupon["_id"] = str(coupon["_id"])
	return coupons