"""Schema for Organisation Management"""


from pydantic import BaseModel, EmailStr, Field
from backend.lib.utils.enums import (
    OrgRole,
)
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


class OrganizationCreate(BaseModel):
    """Schema for creating a new organization."""
    name: str = Field(..., min_length=3, max_length=100)
