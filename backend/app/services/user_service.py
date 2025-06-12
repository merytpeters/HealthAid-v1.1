"""User Service: Handles business logic"""
from typing import Literal
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.lib.crud import create_user, get_user_by_email, get_user_by_id
from backend.lib.utils.user import (
    create_access_token,
    verify_password,
    is_strong_password,
    get_current_user,
    create_refresh_token
)
from backend.lib.errorlib.auth import (
    WeakPasswordException,
    PasswordException,
    UserNotAuthorizedException,
    TokenException,
    UserAlreadyExistsException,
    UserNotFoundException
)


def register_user(
    db: Session, user_data: dict
) -> tuple[User, str, str, Literal["bearer"]]:
    """Register User Service"""
    email = user_data.get("email")
    if email:
        user_data["email"] = email.strip().lower()

    if not is_strong_password(user_data["password"]):
        raise WeakPasswordException()
    
    existing_user = get_user_by_email(db, user_data["email"])
    if existing_user:
        raise UserAlreadyExistsException

    user = create_user(db, **user_data)
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    token_type = "bearer"
    return user, access_token, refresh_token, token_type


def register_user_service_with_response(db: Session, user_data: dict, client_type: str):
    user, access_token, refresh_token, token_type = register_user(db, user_data)

    if client_type == "web":
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": token_type,
            "set_cookies": True,
        }
    else:
        # For mobile, no cookie setting needed
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": token_type,
            "set_cookies": False,
        }



def login_user(
    db: Session, email: str, password: str
) -> tuple[User, str, str, Literal["bearer"]]:
    """Authenticate user and generate token"""
    normalized_email = email.strip().lower()
    user = get_user_by_email(db, normalized_email)
    if not user:
        raise UserNotFoundException()
    if (
        not isinstance(user.hashed_password, str)
        or not verify_password(password, user.hashed_password)
    ):
        raise PasswordException()
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    token_type = "bearer"
    return user, access_token, refresh_token, token_type


def login_user_service_with_response(db: Session, email: str, password: str, client_type: str):
    user, access_token, refresh_token, token_type = login_user(db, email, password)

    if client_type == "web":
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": token_type,
            "set_cookies": True,
        }
    else:
        # For mobile, no cookie setting needed
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": token_type,
            "set_cookies": False,
        }


def get_current_user_from_db(token: str, db: Session) -> tuple[User, str]:
    """Fetch the current user from the db using the provided user data."""
    credentials_exception = TokenException(401, "Invalid or expired token.")
    user_exception = UserNotAuthorizedException()

    if not isinstance(token, str) or not token:
        raise credentials_exception
    user = get_current_user(token, credentials_exception)
    db_user = get_user_by_id(db, user["id"])

    if not db_user:
        raise user_exception

    return db_user, str(db_user.email)
