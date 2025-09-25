"""Schemas for user management."""

from typing import Literal, Optional, Union
from pydantic import BaseModel, EmailStr, Field
from backend.lib.utils.enums import UserType, SubscriptionTier, Currency
from backend.app.schemas.org import OrganizationOut, OrgMemberOut
from backend.app.schemas.admin import AdminOut


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    account_type: Literal["user"]
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
    user_type: UserType

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
    login_context: Literal["user", "organization", "admin"] = "user"


class AuthenticatedUserOut(BaseModel):
    """Authenticated Schema for all user types"""

    user: Union[UserOut, OrgMemberOut, AdminOut, OrganizationOut]
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Literal["bearer"]


class LogoutResponse(BaseModel):
    """Schema for all user type logout"""

    message: str
    token_invalidated: bool


class TokenRefresh(BaseModel):
    """Schema for refresh token"""

    refresh_token: str


class TokenResponse(BaseModel):
    """Token response Schema"""

    access_token: str
    token_type: Literal["bearer"]
