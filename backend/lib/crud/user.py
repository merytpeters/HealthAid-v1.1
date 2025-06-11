"""User CRUD Operations."""
from sqlalchemy.orm import Session
from backend.lib.utils.user import hash_password
from backend.lib.errorlib.auth import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from backend.app.models.user import User


def create_user(db: Session, **kwargs) -> User:
    """Create a new user."""
    email = kwargs.get("email")
    if not email:
        raise ValueError("Email is required")

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise UserAlreadyExistsException(
            f"User with email {email} already exists"
        )

    password = kwargs.pop("password", None)
    if not password:
        raise ValueError("Password is required")

    hashed_pw = hash_password(password)
    # Build new_user with kwargs, but override hashed_password
    new_user = User(**kwargs, hashed_password=hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int) -> User:
    """Fetch a user by their ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException
    return user


def get_user_by_email(db: Session, email: str) -> User:
    """Fetch a user by their email."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise UserNotFoundException(f"User with email {email} not found")
    return user


def update_user(db: Session, user_id: int, **kwargs) -> User:
    """Update an existing user's details."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException

    # Handle password hashing separately
    if "password" in kwargs and kwargs["password"] is not None:
        kwargs["hashed_password"] = hash_password(kwargs.pop("password"))

    # Update other attributes if they are not None
    for key, value in kwargs.items():
        if value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> dict:
    """Delete a user by their ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException

    db.delete(user)
    db.commit()
    return {"detail": f"User with ID {user_id} deleted successfully"}
