"""Schema for admin management"""

from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr
from backend.lib.utils.enums import UserType


class AdminCreate(BaseModel):
    """Schema for creating an admin."""

    account_type: Literal["admin"]
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserType = UserType.ADMIN
    is_admin: Literal["true"] = "true"


class AdminOut(BaseModel):
    """Schema for outputting admin information."""

    id: int
    name: str
    email: str
    role: UserType
    is_admin: Literal["true"]

    model_config = {"from_attributes": True}
