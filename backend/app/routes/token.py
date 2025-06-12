"""Token, Logout Route"""
import os
from jose import jwt, JWTError
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Request,
    Response
)
from datetime import datetime
from backend.app.schemas.user import (
    TokenResponse,
    TokenRefresh,
    LogoutResponse
)
from backend.lib.errorlib.auth import TokenException
from backend.lib.utils.user import (
    token_refresh,
    blacklist_token,
    verify_access_token,
    delete_auth_cookies
)


SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"

router = APIRouter()


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: TokenRefresh):
    """Token refresh"""
    new_access_token = token_refresh(data.refresh_token, TokenException())
    return TokenResponse(access_token=new_access_token, token_type="bearer")


@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response):
    """Logout"""
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_invalidated = False

    # Blacklist access token
    if access_token:
        try:
            payload = verify_access_token(access_token, credentials_exception)
            jti = payload.get("jti")
            exp = payload.get("exp")
            if jti and exp:
                expires_in = max(0, int(exp - datetime.now().timestamp()))
                blacklist_token(jti, expires_in)
                token_invalidated = True
        except HTTPException:
            # Token invalid or blacklisted already, skip blacklisting
            pass

    # Blacklist refresh token
    if refresh_token:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            jti = payload.get("jti")
            exp = payload.get("exp")
            if jti and exp:
                expires_in = max(0, int(exp - datetime.now().timestamp()))
                blacklist_token(jti, expires_in)
                token_invalidated = True
        except JWTError:
            pass

    # Delete cookies
    delete_auth_cookies(response)

    return LogoutResponse(message="Logout successful!", token_invalidated=token_invalidated)
