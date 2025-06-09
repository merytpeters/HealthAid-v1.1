"""User Crud Operations."""
from sqlalchemy.orm import Session
from backend.lib.utils.user import hash_password
from backend.lib.errorlib.auth import (
    UserNotFoundException,
    UserAlreadyExistsException,
)

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: int):
    """Fetch a user by their ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException
    return user

def create_user(db: Session, user_data: UserCreate):
    """Create a new user."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise UserAlreadyExistsException

    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        full_name = user_data.full_name,
        hashed_password = hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """Update an existing user's details."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException

    if user_data.username:
        user.username = user_data.username
    if user_data.email:
        user.email = user_data.email
    if user_data.full_name:
        user.full_name = user_data.full_name
    if user_data.password:
        user.hashed_password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    return user

def delete_user():
    """Delete User"""
