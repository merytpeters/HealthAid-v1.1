"""User and Organization models for the application."""

from __future__ import annotations
import uuid as uuid_lib
from sqlalchemy import Column, String, Enum, ForeignKey, UUID, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from backend.app.models.base import Base
from backend.lib.utils.enums import UserType, SubscriptionTier, Currency, OrgRole
from backend.app.models.individual_users.user_dashboard import UserDashboard


class User(Base):
    """User model representing a user in the system."""

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid_lib.uuid4()),
        index=True,
        autoincrement=False,
    )
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), default=UserType.USER, nullable=False)

    organization_id = Column(
        UUID(as_uuid=False), ForeignKey("organizations.id"), nullable=True
    )
    organization = relationship("Organization", back_populates="users")

    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    currency = Column(Enum(Currency), default=Currency.USD)

    assigned_staff_id = Column(
        UUID(as_uuid=False),
        ForeignKey("org_members.id", use_alter=True, name="fk_user_assigned_staff_id"),
        nullable=True,
    )
    assigned_staff = relationship(
        "OrgMember",
        back_populates="assigned_patients",
        foreign_keys=[assigned_staff_id],
        uselist=False,
    )
    dashboard = relationship("UserDashboard", uselist=False, back_populates="user")

    def __repr__(self):
        """String representation of the User model."""
        return f"<User(id={self.id}, username={self.username}, " f"email={self.email})>"


class Organization(Base):
    """Organization model representing an organization in the system."""

    __tablename__ = "organizations"

    id = Column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid_lib.uuid4()),
        index=True,
        autoincrement=False,
    )
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    users = relationship("User", back_populates="organization")
    user_type = Column(Enum(UserType), default=UserType.ORGANIZATION)
    role = Column(Enum(OrgRole), default=OrgRole.ORG_ADMIN)

    @property
    def is_admin(self):
        """Check if organization has admin role"""
        return self.role == OrgRole.ORG_ADMIN

    def __repr__(self):
        """
        Returns a string representation of the Organization
        instance, including its id and name.
        Returns:
            str: A formatted string displaying the organization's
            id and name.
        """
        return f"<Organization(id={self.id}, name={self.name})>"


class OrgMember(Base):
    """Organization Member model representing a member of an organization."""

    __tablename__ = "org_members"

    id = Column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid_lib.uuid4()),
        index=True,
        autoincrement=False,
    )
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    organization_id = Column(UUID(as_uuid=False), ForeignKey("organizations.id"))
    role = Column(Enum(OrgRole), default=OrgRole.STAFF)
    user = relationship("User", foreign_keys=[user_id])
    username = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    organization = relationship("Organization")
    is_active = Column(Boolean, default=True, nullable=False)
    joined_at = Column(DateTime, default=func.now(), nullable=False)
    assigned_patients = relationship(
        "User", back_populates="assigned_staff", foreign_keys="User.assigned_staff_id"
    )

    def __repr__(self):
        """
        Return a string representation of the OrgMember instance,
        including its id, user_id, and organization_id.
        """
        return (
            f"<OrgMember(id={self.id}, user={self.user}, "
            f"organization={self.organization})>"
        )


class Admin(Base):
    """Healthaid App Admin"""

    __tablename__ = "admin"

    id = Column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid_lib.uuid4()),
        index=True,
        autoincrement=False,
    )
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), default=UserType.ADMIN, nullable=False)
    is_admin = Column(String, default="true", nullable=False)

    def __repr__(self):
        """
        Return a string representation of the Admin object,
        including id, name, role, and is_admin status.
        """
        return (
            f"<Admin(id={self.id}, name={self.name},"
            f"usertype={self.user_type}, is_admin={self.is_admin})>"
        )
