"""User profile API"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.schemas.auth import AuthenticatedUserOut
from backend.lib.errorlib.auth import UserNotAuthorizedException
from backend.app.services.auth_service import (
    get_current_user_from_db as profile_service,
)
from backend.app.dependencies.security import user_oauth2_scheme
from backend.app.db.session import get_db


router = APIRouter()


@router.get("/profile", response_model=AuthenticatedUserOut)
def profile(db: Session = Depends(get_db), token: str = Depends(user_oauth2_scheme)):
    """User Profile"""
    try:
        user, _ = profile_service(token, db)
        return user
    except UserNotAuthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e
