"""Schema for Organisation Management"""

from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from lib.utils.enums import OrgRole, UserType
from app.api.v1.auth.schemas.user.user import UserOut


class OrganizationCreate(BaseModel):
    """Schema for creating a new organization."""

    account_type: Literal["organization"]
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


class OrganizationOut(BaseModel):
    """Schema for outputting organization information."""

    id: str
    name: str
    email: str
    user_type: UserType = UserType.ORGANIZATION
    role: OrgRole = OrgRole.ORG_ADMIN

    model_config = {"from_attributes": True}


class OrganizationWithRoleOut(OrganizationOut):
    """Out Schema for OrgRoles"""

    org_role: OrgRole


class OrgMemberCreate(BaseModel):
    """Schema for creating a new organization member."""

    account_type: Literal["org_member"]
    user_id: Optional[str] = Field(
        None, description="Optional User ID to link existing patient"
    )
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., max_length=100)
    organization_id: str = Field(..., description="Organization ID to join")
    role: OrgRole = Field(default=OrgRole.STAFF, description="Role in organization")


class OrgMemberJoinExisting(BaseModel):
    """Schema for adding existing org_member to another organization."""

    existing_member_email: EmailStr = Field(
        ..., description="Email of existing org member"
    )
    organization_id: str = Field(..., description="Organization ID to join")
    role: OrgRole = Field(default=OrgRole.STAFF, description="Role in new organization")


class OrgMemberOut(BaseModel):
    """Schema for outputting organization member information."""

    id: str
    user_id: Optional[str] = None
    username: str
    email: str
    full_name: str
    organization_id: str
    role: OrgRole
    is_active: bool = True
    joined_at: datetime  # Use datetime instead of str
    user: Optional["UserOut"] = None

    model_config = {"from_attributes": True}


class OrgMembershipList(BaseModel):
    """Schema for listing all organization memberships for a user."""

    user_id: Optional[str] = None
    email: str
    memberships: list[OrgMemberOut]


class OrgMemberUpdate(BaseModel):
    """Schema for updating organization member."""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    role: Optional[OrgRole] = None
