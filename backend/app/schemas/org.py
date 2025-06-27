"""Schema for Organisation Management"""
from typing import Literal
from pydantic import BaseModel, EmailStr, Field
from backend.lib.utils.enums import (
    OrgRole,
    UserType
)


class OrganizationCreate(BaseModel):
    """Schema for creating a new organization."""
    account_type: Literal["organization"]
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


class OrganizationOut(BaseModel):
    """Schema for outputting organization information."""
    id: int
    name: str
    email: str
    user_type: UserType = UserType.ORGANIZATION

    model_config = {"from_attributes": True}


class OrganizationWithRoleOut(OrganizationOut):
    """Out Schema for OrgRoles"""
    org_role: OrgRole


class OrgMemberCreate(BaseModel):
    """Schema for creating a new organization member."""
    user_id: int
    organization_id: int
    role: OrgRole = OrgRole.STAFF


class OrgMemberOut(BaseModel):
    """Schema for outputting organization member information."""
    id: int
    user_id: int
    organization_id: int
    role: OrgRole

    model_config = {"from_attributes": True}
