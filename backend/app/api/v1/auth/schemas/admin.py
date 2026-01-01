"""Schema for admin management"""

from typing import Literal
from pydantic import BaseModel, Field, EmailStr
from lib.utils.enums import UserType


class AdminCreate(BaseModel):
    """Schema for creating an admin."""

    account_type: Literal["admin"]
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


class AdminOut(BaseModel):
    """Schema for outputting admin information."""

    id: str
    name: str
    email: str
    user_type: UserType
    is_admin: Literal["true"]

    model_config = {"from_attributes": True}
