"""
Authorization and authentication APIs
Token, Logout Route"""

import os
from typing import cast
from datetime import datetime
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException, status, Request, Response, Depends
from sqlalchemy.orm import Session
from backend.app.api.v1.auth.schemas.auth import (
    TokenResponse,
    TokenRefresh,
    LogoutResponse,
    AuthenticatedUserOut,
)
from backend.lib.utils.user import (
    token_refresh,
    blacklist_token,
    verify_access_token,
    delete_auth_cookies,
)
from backend.lib.utils.clienttype import ClientType
from backend.app.api.v1.auth.schemas.user.user import UserLogin
from backend.lib.errorlib.auth import (
    UserNotFoundException,
    PasswordException,
    TokenException,
)
from backend.app.api.v1.auth.services.auth_service import (
    login_user_service_with_response as login_user_service,
)
from backend.app.api.db.session import get_db
from backend.app.api.v1.auth.services.auth_service import (
    register_user_service_with_response as register_user_service,
)
from backend.app.api.v1.auth.schemas import RegisterSchema


SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: TokenRefresh):
    """Token refresh"""
    new_access_token = token_refresh(data.refresh_token, TokenException())
    return TokenResponse(access_token=new_access_token, token_type="bearer")


@router.post(
    "/register",
    response_model=AuthenticatedUserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: RegisterSchema,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
):
    """Register All user/usertypes"""
    client_type_raw = request.headers.get("X-Client-Type", "web")

    user_data = payload.model_dump(exclude_unset=True)
    account_type = user_data.pop("account_type", "user")

    result = register_user_service(
        db, user_data, client_type_raw=client_type_raw, account_type=account_type
    )

    auth_out = AuthenticatedUserOut(
        user=result["user"],
        access_token=None if result["set_cookies"] else result["access_token"],
        refresh_token=None if result["set_cookies"] else result["refresh_token"],
        token_type=result["token_type"],
    )

    if result["set_cookies"]:
        response.set_cookie(
            "access_token",
            result["access_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=15 * 60,
        )
        response.set_cookie(
            "refresh_token",
            result["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,
        )

    return auth_out


@router.post(
    "/login", response_model=AuthenticatedUserOut, status_code=status.HTTP_200_OK
)
async def login(
    user_login: UserLogin,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
):
    """Login For all User Types"""
    try:
        client_type_raw = request.headers.get("X-Client-Type", "web")

        client_type: ClientType = cast(ClientType, client_type_raw)

        login_context = user_login.login_context

        result = login_user_service(
            db=db,
            email=user_login.email,
            password=user_login.password,
            client_type_raw=client_type,
            login_context=login_context,
        )

        if result["set_cookies"]:
            response.set_cookie(
                "access_token",
                result["access_token"],
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=15 * 60,
            )
            response.set_cookie(
                "refresh_token",
                result["refresh_token"],
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=7 * 24 * 60 * 60,
            )

            # Return without tokens in JSON since they are in cookies
            return {
                "user": result["user"],
                "access_token": None,
                "refresh_token": None,
                "token_type": result["token_type"],
            }

        # Return full response with tokens in JSON
        return {
            "user": result["user"],
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": result["token_type"],
        }
    except UserNotFoundException as exc:
        raise HTTPException(status_code=401, detail="User not found") from exc
    except PasswordException as exc:
        raise HTTPException(status_code=401, detail="Invalid credentials") from exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


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

    return LogoutResponse(
        message="Logout successful!", token_invalidated=token_invalidated
    )
