"""Shared Auth CRUD"""

from typing import Union

from app.api.v1.auth.models.user import Admin, Organization, OrgMember, User
from lib.errorlib.auth import UserNotFoundException
from sqlalchemy.orm import Session


def get_user_by_id(
    db: Session, user_id: str
) -> Union[User, OrgMember, Organization, Admin]:
    """Fetch any account type by their ID."""

    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user

    org_member = db.query(OrgMember).filter(OrgMember.id == user_id).first()
    if org_member:
        return org_member

    organization = db.query(Organization).filter(Organization.id == user_id).first()
    if organization:
        return organization

    admin = db.query(Admin).filter(Admin.id == user_id).first()
    if admin:
        return admin

    raise UserNotFoundException(f"No account found with ID: {user_id}")


def get_user_by_id_and_type(
    db: Session, user_id: str, user_type: str
) -> Union[User, OrgMember, Organization, Admin]:
    """Fetch account by ID and type (more efficient)."""

    if user_type == "user":
        user = db.query(User).filter(User.id == user_id).first()
    elif user_type == "org_member":
        user = db.query(OrgMember).filter(OrgMember.id == user_id).first()
    elif user_type == "organization":
        user = db.query(Organization).filter(Organization.id == user_id).first()
    elif user_type == "admin":
        user = db.query(Admin).filter(Admin.id == user_id).first()
    else:
        raise ValueError(f"Invalid user_type: {user_type}")

    if not user:
        raise UserNotFoundException(f"No {user_type} found with ID: {user_id}")

    return user
