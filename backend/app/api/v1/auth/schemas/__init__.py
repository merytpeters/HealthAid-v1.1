"""Schema Initialization"""

from typing import Union, Annotated
from pydantic import Field
from .admin import AdminCreate
from .org import OrganizationCreate, OrgMemberCreate
from .user.user import UserCreate

RegisterSchema = Annotated[
    Union[UserCreate, OrganizationCreate, AdminCreate, OrgMemberCreate],
    Field(discriminator="account_type"),
]
