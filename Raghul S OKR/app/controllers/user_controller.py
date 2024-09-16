# app/controllers/user_controller.py
from app.models.user_model import UserSchema
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.config.database import db
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime, timedelta

async def create_user(user_data: UserSchema):
    user = await db["users"].find_one({"email": user_data.email})
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data.password = hash_password(user_data.password)
    await db["users"].insert_one(user_data.dict(by_alias=True))
    return user_data

async def authenticate_user(email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_user_by_id(user_id: str):
    user = await db["users"].find_one({"_id": ObjectId(user_id), "is_deleted": False})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Convert ObjectId to string
    user["id"] = str(user["_id"])
    return UserSchema(**user)

async def get_all_users():
    users = await db["users"].find({"is_deleted": False}).to_list(length=None)
    # Convert ObjectId to string for each user
    for user in users:
        user["id"] = str(user["_id"])
    return [UserSchema(**{**user, "_id": str(user["_id"])}) for user in users]

async def update_user(user_id: str, update_data: dict):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data["updated_at"] = datetime.utcnow()
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return await get_user_by_id(user_id)

async def delete_user(user_id: str):
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"is_deleted": True}})
    return {"message": "User deleted successfully"}
