"""Staff CRUD operations."""

from sqlalchemy.orm import Session, joinedload
from backend.app.api.v1.auth.models.user import User, OrgMember
from backend.lib.utils.user import hash_password
from backend.lib.errorlib.auth import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from backend.app.api.v1.auth.crud.users.user import create_user
from backend.lib.utils.enums import OrgRole


def create_org_member_directly(db: Session, **kwargs) -> OrgMember:
    """Create org member directly (for org_member account registration)"""

    if "password" in kwargs:
        kwargs["hashed_password"] = hash_password(kwargs.pop("password"))

    # user_id is None for direct registration
    kwargs["user_id"] = None

    org_member = OrgMember(**kwargs)

    db.add(org_member)
    db.commit()
    db.refresh(org_member)
    return org_member


def get_org_member_by_email(db: Session, email: str) -> OrgMember | None:
    """Get org member by email (for login)"""
    return (
        db.query(OrgMember)
        .filter(OrgMember.email == email)
        .options(joinedload(OrgMember.user), joinedload(OrgMember.organization))
        .first()
    )


def add_existing_user_to_org(
    db: Session, user_id: str, organization_id: str, role: OrgRole = OrgRole.STAFF
) -> OrgMember:
    """Add existing user to an organization"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException("User not found")

    existing_membership = (
        db.query(OrgMember)
        .filter(
            OrgMember.user_id == user_id, OrgMember.organization_id == organization_id
        )
        .first()
    )

    if existing_membership:
        raise UserAlreadyExistsException("User already a member of this organization")

    new_membership = OrgMember(
        user_id=user_id,
        organization_id=organization_id,
        role=role,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.hashed_password,
    )

    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership


def create_user_and_add_to_org(db: Session, **kwargs) -> OrgMember:
    """Create new user and add to organization"""

    organization_id = kwargs.pop("organization_id")
    role = kwargs.pop("role", OrgRole.STAFF)

    new_user = create_user(db, **kwargs)

    user_id = str(new_user.id) if new_user.id is not None else None
    if user_id is None:
        raise ValueError("User creation failed - no ID assigned")

    return add_existing_user_to_org(db, user_id, organization_id, role)


def get_user_organizations(db: Session, user_id: str):
    """Get all organizations a user belongs to"""
    return (
        db.query(OrgMember)
        .options(joinedload(OrgMember.organization))
        .filter(OrgMember.user_id == user_id)
        .all()
    )


def get_org_members_by_organization(db: Session, organization_id: str):
    """Get all members of an organization (both linked and independent)"""
    return (
        db.query(OrgMember)
        .filter(OrgMember.organization_id == organization_id)
        .options(joinedload(OrgMember.user), joinedload(OrgMember.organization))
        .all()
    )


def remove_user_from_org(db: Session, user_id: str, organization_id: str) -> dict:
    """Remove a user from an organization"""
    membership = (
        db.query(OrgMember)
        .filter(
            OrgMember.user_id == user_id, OrgMember.organization_id == organization_id
        )
        .first()
    )

    if not membership:
        raise UserNotFoundException("User is not a member of this organization")

    db.delete(membership)
    db.commit()
    return {"detail": f"User {user_id} removed from organization {organization_id}"}


def update_user_role_in_org(
    db: Session, user_id: str, organization_id: str, new_role: OrgRole
) -> OrgMember:
    """Update a user's role in an organization"""
    membership = (
        db.query(OrgMember)
        .filter(
            OrgMember.user_id == user_id, OrgMember.organization_id == organization_id
        )
        .first()
    )

    if not membership:
        raise UserNotFoundException("User is not a member of this organization")

    setattr(membership, "role", new_role)
    db.commit()
    db.refresh(membership)
    return membership
