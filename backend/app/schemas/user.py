"""Schemas for user and organization management."""
from typing import Literal
from pydantic import BaseModel, EmailStr, Field
from backend.lib.utils.enums import (
    UserType,
    OrgRole,
    SubscriptionTier,
    Currency
)


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str | None = Field(None, max_length=100)


class UserOut(BaseModel):
    """Schema for outputting user information."""
    id: int
    username: str
    email: str
    full_name: str

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


class AuthenticatedUserOut(BaseModel):
    """Schema for authenticated user"""
    user: UserOut
    access_token: str
    token_type: Literal["bearer"]


class OrganizationCreate(BaseModel):
    """Schema for creating a new organization."""
    name: str = Field(..., min_length=3, max_length=100)


class OrganizationOut(BaseModel):
    """Schema for outputting organization information."""
    id: str
    name: str

    model_config = {"from_attributes": True}


class OrgMemberCreate(BaseModel):
    """Schema for creating a new organization member."""
    user_id: str
    organization_id: str
    role: OrgRole = OrgRole.STAFF


class OrgMemberOut(BaseModel):
    """Schema for outputting organization member information."""
    id: str
    user_id: str
    organization_id: str
    role: OrgRole = OrgRole.STAFF

    model_config = {"from_attributes": True}
