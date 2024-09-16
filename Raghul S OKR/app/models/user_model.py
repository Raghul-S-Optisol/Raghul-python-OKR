# app/models/user_model.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from app.config.database import PyObjectId
from bson import ObjectId
from datetime import datetime

class UserSchema(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    is_deleted: bool = False
    is_admin: bool = False
    password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @validator('id', pre=True, always=True)
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "phone_number": 1234567890,
                "is_admin": False,
                "password": "password123",
            }
        }
