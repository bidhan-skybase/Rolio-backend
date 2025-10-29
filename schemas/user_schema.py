from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    """Schema for creating a new user - only email needed"""
    email: EmailStr


class UserDelete(BaseModel):
    """Schema for deleting a user"""
    id: int
    email: EmailStr


class UserResponse(BaseModel):
    """Schema for user responses"""
    model_config = ConfigDict(from_attributes=True) 
    
    id: int
    email: str
    created_at: datetime