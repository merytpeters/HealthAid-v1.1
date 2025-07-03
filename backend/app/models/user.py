"""User and Organization models for the application."""
from __future__ import annotations
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models.base import Base
from backend.lib.utils.enums import (
    UserType,
    SubscriptionTier,
    Currency,
    OrgRole
)


class User(Base):
    """User model representing a user in the system."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), default=UserType.USER, nullable=False)

    organization_id = Column(
        Integer, ForeignKey("organizations.id"), nullable=True
    )
    organization = relationship("Organization", back_populates="users")

    subscription_tier = Column(
        Enum(SubscriptionTier), default=SubscriptionTier.FREE
    )
    currency = Column(Enum(Currency), default=Currency.USD)

    assigned_staff_id = Column(
        Integer,
        ForeignKey(
            "org_members.id",
            use_alter=True,
            name="fk_user_assigned_staff_id"
        ),
        nullable=True
    )
    assigned_staff = relationship(
        "OrgMember",
        back_populates="assigned_patients",
        foreign_keys=[assigned_staff_id],
        uselist=False
    )
    dashboard = relationship("UserDashboard", uselist=False, back_populates="user")

    def __repr__(self):
        """String representation of the User model."""
        return (
            f"<User(id={self.id}, username={self.username}, "
            f"email={self.email})>"
        )


class Organization(Base):
    """Organization model representing an organization in the system."""
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    users = relationship("User", back_populates="organization")

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

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    role = Column(Enum(OrgRole), default=OrgRole.STAFF)
    user = relationship(
        "User",
        foreign_keys=[user_id]
    )
    organization = relationship("Organization")
    assigned_patients = relationship(
        "User",
        back_populates="assigned_staff",
        foreign_keys=[User.assigned_staff_id]
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

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserType), default=UserType.ADMIN, nullable=False)
    is_admin = Column(String, default="true", nullable=False)

    def __repr__(self):
        """
        Return a string representation of the Admin object,
        including id, name, role, and is_admin status.
        """
        return (
            f"<Admin(id={self.id}, name={self.name},"
            f"role={self.role}, is_admin={self.is_admin})>"
        )
