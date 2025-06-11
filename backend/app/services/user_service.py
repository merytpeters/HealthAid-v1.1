"""User Service: Handles business logic"""
from typing import Literal
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.lib.crud import create_user, get_user_by_email, get_user_by_id
from backend.lib.utils.user import (
    create_access_token,
    verify_password,
    is_strong_password,
    get_current_user
)
from backend.lib.errorlib.auth import WeakPasswordException, PasswordException


def register_user(
    db: Session, user_data: dict
) -> tuple[User, str, Literal["bearer"]]:
    """Register User Service"""
    email = user_data.get("email")
    if email:
        user_data["email"] = email.strip().lower()

    if not is_strong_password(user_data["password"]):
        raise WeakPasswordException("Password is not strong enough")

    user = create_user(db, **user_data)
    token = create_access_token(data={"sub": user.email})
    token_type = "bearer"
    return user, token, token_type


def login_user(
    db: Session, email: str, password: str
) -> tuple[User, str, Literal["bearer"]]:
    """Authenticate user and generate token"""
    normalized_email = email.strip().lower()
    user = get_user_by_email(db, normalized_email)
    if (
        not user or not isinstance(user.hashed_password, str)
        or not verify_password(password, user.hashed_password)
    ):
        raise PasswordException("Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    token_type = "bearer"
    return user, token, token_type

# def get_current_user_from_db():
    """Profile Service"""
