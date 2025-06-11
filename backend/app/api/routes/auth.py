"""Authorization and authentication APIs"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.app.schemas.user import (
    UserCreate,
    AuthenticatedUserOut,
    UserLogin
)
from backend.app.db.session import get_db
from backend.lib.errorlib.auth import (
    PasswordException,
    WeakPasswordException
)
from backend.app.services.user_service import (
    register_user as register_user_service
)
from backend.app.services.user_service import login_user as login_user_service


router = APIRouter(prefix="/auth")
"""Regular User API"""


@router.post(
    "/user/register",
    response_model=AuthenticatedUserOut,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_create: UserCreate, db: Session = Depends(get_db)
):
    """Register regular user"""
    try:
        user, token, token_type = register_user_service(
            db, user_create.model_dump(exclude_unset=True)
        )
    except WeakPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    return {
        "user": user,
        "access_token": token,
        "token_type": token_type,
    }


@router.post(
    "/user/login",
    response_model=AuthenticatedUserOut,
    status_code=status.HTTP_202_ACCEPTED
)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Login User"""
    try:
        user, token, token_type = login_user_service(
            db, user_login.email, user_login.password
        )
    except PasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e
    return {
        "user": user,
        "access_token": token,
        "token_type": token_type,
    }


"""Admin API"""


"""Org API"""


"""Org Staff API"""
