# backend/models/notice_model.py (updated)
from datetime import datetime
from backend.config import db

notice_collection = db["notices"]  # Access the 'notices' collection

def create_notice(data):
    """Insert a new notice into MongoDB and return inserted id as string"""
    data["created_at"] = datetime.utcnow()
    result = notice_collection.insert_one(data)
    return str(result.inserted_id)

def get_all_notices(user_id=None):
    """
    Retrieve all notices for a given user_id or all notices.
    """
    query = {}
    if user_id:
        query = {"$or": [{"user_id": user_id}, {"user_id": None}]}
    else:
        query = {}

    notices = list(notice_collection.find(query))
    for n in notices:
        n["_id"] = str(n["_id"])  # Convert ObjectId to string
    return notices

def delete_notice(notice_id):
    from bson import ObjectId
    res = notice_collection.delete_one({"_id": ObjectId(notice_id)})
    return res.deleted_count

def mark_notice_completed(notice_id):
    from bson import ObjectId
    res = notice_collection.update_one(
        {"_id": ObjectId(notice_id)},
        {"$set": {"status": "completed", "completedDate": datetime.utcnow().strftime("%Y-%m-%d")}}
    )
    return res.modified_count

