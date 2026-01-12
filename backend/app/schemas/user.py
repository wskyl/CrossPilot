"""
User schemas for API request/response
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from ..models.user import SubscriptionPlan


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for user profile update"""
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    avatar_url: Optional[str]
    subscription_plan: SubscriptionPlan
    monthly_conversions_used: int
    monthly_conversions_limit: int
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
