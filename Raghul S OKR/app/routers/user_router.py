# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.user_model import UserSchema
from app.controllers.user_controller import create_user, authenticate_user, get_user_by_id, get_all_users, update_user, delete_user
from app.services.auth_service import get_current_user
from app.services.auth_service import OAuth2PasswordRequestFormEmail
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

router = APIRouter()

@router.post("/signup", response_model=UserSchema)
async def signup(user: UserSchema):
    return await create_user(user)

@router.post("/signin")
async def signin(form_data: OAuth2PasswordRequestFormEmail = Depends()):
    return await authenticate_user(form_data.email, form_data.password)

@router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(user_id: str, current_user: str = Depends(get_current_user)):
    return await get_user_by_id(user_id)

@router.get("/users", response_model=List[UserSchema])
async def list_users(current_user: str = Depends(get_current_user)):
    return await get_all_users()

@router.put("/user/{user_id}", response_model=UserSchema)
async def update_user_route(user_id: str, update_data: dict, current_user: str = Depends(get_current_user)):
    return await update_user(user_id, update_data)

@router.delete("/user/{user_id}")
async def delete_user_route(user_id: str, current_user: str = Depends(get_current_user)):
    return await delete_user(user_id)
