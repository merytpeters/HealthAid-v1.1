"""Authentication schemas"""

from typing import Literal, Optional, Union
from pydantic import BaseModel
from backend.app.schemas.user.user import UserOut
from backend.app.schemas.org import OrgMemberOut, OrganizationOut
from backend.app.schemas.admin import AdminOut


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
