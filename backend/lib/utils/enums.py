"""Enums for user types, organization roles,
subscription tiers, and currencies."""
from enum import Enum


class UserType(str, Enum):
    """Enums for user types"""
    ADMIN = "admin"
    USER = "user"
    ORGANIZATION = "organization"


class OrgRole(str, Enum):
    """Enums for organization roles"""
    ORG_ADMIN = "org_admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    STAFF = "staff"


class SubscriptionTier(str, Enum):
    """Enums for subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"


class Currency(str, Enum):
    """Enums for currencies"""
    USD = "USD"
    NGN = "NGN"
    EUR = "EUR"
