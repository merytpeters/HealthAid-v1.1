"""Schema Initialization"""

from typing import Union, Annotated
from pydantic import Field
from .admin import AdminCreate
from .org import OrganizationCreate
from .user.user import UserCreate

RegisterSchema = Annotated[
    Union[UserCreate, OrganizationCreate, AdminCreate],
    Field(discriminator="account_type"),
]
