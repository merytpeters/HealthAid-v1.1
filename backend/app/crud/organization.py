"""Organization CRUD operations."""

from sqlalchemy.orm import Session, joinedload
from backend.app.models.user import User, OrgMember, Organization
from backend.lib.utils.user import hash_password
from backend.lib.errorlib.auth import (
    UserNotFoundException,
    UserAlreadyExistsException,
)


def create_organization_with_email(db: Session, **kwargs) -> Organization:
    """Create organization"""
    email = kwargs.get("email")
    if not email:
        raise ValueError("Email is required")

    existing_organization = (
        db.query(Organization).filter(Organization.email == email).first()
    )
    if existing_organization:
        raise UserAlreadyExistsException(
            f"Organization with email {email} already exists"
        )

    password = kwargs.pop("password", None)
    if not password:
        raise ValueError("Password is required")

    hashed_pw = hash_password(password)
    # Build new_org with kwargs, but override hashed_password
    new_org = Organization(**kwargs, hashed_password=hashed_pw)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org


def get_organization_by_id(db: Session, organization_id=str) -> Organization:
    """Get organizations by id"""
    organization = (
        db.query(Organization).filter(Organization.id == organization_id).first()
    )
    if not organization:
        raise UserNotFoundException()
    return organization


def get_organization_by_email(db: Session, email: str) -> Organization:
    """Get Org by email"""
    return db.query(Organization).filter(Organization.email == email).first()


def add_admin():
    pass


def promote_to_admin():
    pass


def remove_admin():
    pass


def update_organization():
    pass


def org_admin_required():
    pass


def get_organization_staff(db: Session, organization_id: str):
    """Get all staff in an organization"""
    return (
        db.query(OrgMember)
        .options(joinedload(OrgMember.user))
        .filter(OrgMember.organization_id == organization_id)
        .all()
    )


def delete_organization():
    pass
