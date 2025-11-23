from core.database import db
from bson.objectid import ObjectId

def create_review(product_id, user_id, review_data):
	review_dict = review_data.dict()
	review_dict["product_id"] = product_id
	review_dict["user_id"] = user_id
	review_dict["is_approved"] = False
	review_dict["helpful"] = []
	result = db["reviews"].insert_one(review_dict)
	review_dict["_id"] = str(result.inserted_id)
	return review_dict

def get_product_reviews(product_id, skip=0, limit=20):
	reviews = list(db["reviews"].find({"product_id": product_id}).skip(skip).limit(limit))
	for review in reviews:
		review["_id"] = str(review["_id"])
	return reviews

def update_review(review_id, user_id, review_update):
	result = db["reviews"].update_one(
		{"_id": ObjectId(review_id), "user_id": user_id},
		{"$set": review_update.dict(exclude_unset=True)}
	)
	if result.modified_count:
		return get_review_by_id(review_id)
	return None

def delete_review(review_id, user_id):
	result = db["reviews"].delete_one({"_id": ObjectId(review_id), "user_id": user_id})
	return result.deleted_count > 0

def mark_review_helpful(review_id, user_id, action):
	review = db["reviews"].find_one({"_id": ObjectId(review_id)})
	if not review:
		return None
	helpful = set(review.get("helpful", []))
	if action == "add":
		helpful.add(user_id)
	elif action == "remove":
		helpful.discard(user_id)
	db["reviews"].update_one({"_id": ObjectId(review_id)}, {"$set": {"helpful": list(helpful)}})
	return get_review_by_id(review_id)

def update_review_approval(review_id, is_approved):
	result = db["reviews"].update_one(
		{"_id": ObjectId(review_id)},
		{"$set": {"is_approved": is_approved}}
	)
	if result.modified_count:
		return get_review_by_id(review_id)
	return None

def get_review_by_id(review_id):
	review = db["reviews"].find_one({"_id": ObjectId(review_id)})
	if review:
		review["_id"] = str(review["_id"])
	return review
