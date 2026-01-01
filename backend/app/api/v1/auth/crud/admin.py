"""Admin Crud operations for the application."""

from sqlalchemy.orm import Session
from app.api.v1.auth.models.user import Admin
from lib.utils.user import hash_password
from lib.errorlib.auth import (
    UserNotFoundException,
    UserAlreadyExistsException,
)


def create_admin(db: Session, **kwargs) -> Admin:
    """Create a single admin (singleton pattern)"""
    # Check if any admin exists
    existing_admin = db.query(Admin).first()
    if existing_admin:
        raise UserAlreadyExistsException("An admin already exists.")

    email = kwargs.get("email")
    if not email:
        raise ValueError("Email is required")

    password = kwargs.pop("password", None)
    if not password:
        raise ValueError("Password is required")

    hashed_pw = hash_password(password)
    admin = Admin(**kwargs, hashed_password=hashed_pw)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def get_admin_by_id(db: Session, admin_id: int) -> Admin:
    """Get admin by id"""
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise UserNotFoundException()
    return admin


def get_admin_by_email(db: Session, email: str) -> Admin:
    """Get admin by email"""
    return db.query(Admin).filter(Admin.email == email).first()
