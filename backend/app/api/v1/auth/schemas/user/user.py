"""Schemas for user management."""

from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field
from backend.lib.utils.enums import UserType, SubscriptionTier, Currency


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    account_type: Literal["user"]
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str | None = Field(None, max_length=100)
    organization_id: Optional[str] = Field(
        None, description="Optional organization ID to associate user with"
    )


class UserOut(BaseModel):
    """Schema for outputting user information."""

    id: str
    username: str
    email: str
    full_name: str
    user_type: UserType
    organization_id: Optional[str] = None

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""

    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    full_name: str | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=8)
    user_type: UserType | None = None
    subscription_tier: SubscriptionTier | None = None
    currency: Currency | None = None
    assigned_staff_id: str | None = None
    assigned_patients: list[str] = []


class UserLogin(BaseModel):
    """Schema for user login."""

    email: str
    password: str = Field(..., min_length=8)
    login_context: Literal["user", "organization", "admin", "org_member"] = "user"
