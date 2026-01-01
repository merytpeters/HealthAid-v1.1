"""User Service: Handles business logic"""

from typing import Literal, Union
from sqlalchemy.orm import Session
from app.api.v1.auth.models.user import User, OrgMember, Organization, Admin
from app.api.v1.auth.crud import (
    create_user,
    get_user_by_email,
    get_org_member_by_email,
    get_organization_by_email,
    create_organization_with_email,
    create_admin,
    get_admin_by_email,
    create_org_member_directly,
    add_existing_user_to_org,
)
from lib.utils.user import (
    create_access_token,
    verify_password,
    is_strong_password,
    create_refresh_token,
)
from lib.utils.clienttype import ClientType, validate_client_type
from lib.errorlib.auth import (
    WeakPasswordException,
    PasswordException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.api.v1.auth.schemas.user.user import UserOut
from app.api.v1.auth.schemas.auth import AuthenticatedUserOut
from app.api.v1.auth.schemas.org import OrgMemberOut, OrganizationOut
from app.api.v1.auth.schemas.admin import AdminOut
from lib.utils.enums import UserType, OrgRole


MODEL_TO_SCHEMA = {
    "User": UserOut,
    "OrgMember": OrgMemberOut,
    "Admin": AdminOut,
    "Organization": OrganizationOut,
}


def to_schema(user_obj):
    """To schema"""
    model_name = user_obj.__class__.__name__
    schema_class = MODEL_TO_SCHEMA.get(model_name)
    if not schema_class:
        raise ValueError(f"Unknown user model type: {model_name}")
    return schema_class.model_validate(user_obj)


def register_account(
    db: Session,
    user_data: dict,
    account_type: Literal["user", "organization", "admin", "org_member"],
) -> AuthenticatedUserOut:
    """Register a User, Organization, or Admin account"""

    # Normalize email
    email = user_data.get("email", "").strip().lower()
    user_data["email"] = email

    if not email:
        raise ValueError("Email is required")
    if not user_data.get("password"):
        raise ValueError("Password is required")
    if not is_strong_password(user_data["password"]):
        raise WeakPasswordException()

    if account_type == "org_member":
        organization_id = user_data.get("organization_id")
        if not organization_id:
            raise ValueError("organization_id is required for org_member registration")

        # For org_members, check if user exists with this email
        existing_user = get_user_by_email(db, email)

        # Check if org_member already exists in the SAME organization with this email
        existing_org_member_same_org = (
            db.query(OrgMember)
            .filter(
                OrgMember.email == email, OrgMember.organization_id == organization_id
            )
            .first()
        )

        existing_org = get_organization_by_email(db, email)
        existing_admin = get_admin_by_email(db, email)

        # If org_member already exists in the SAME organization, deny registration
        if existing_org_member_same_org:
            raise UserAlreadyExistsException(
                "An org member with this email already exists in this organization"
            )

        # If organization or admin exists with this email, deny registration
        if existing_org or existing_admin:
            raise UserAlreadyExistsException(
                "An account with this email already exists"
            )

        if existing_user:
            # Add existing user to organization
            role = user_data.get("role", OrgRole.STAFF)
            if isinstance(role, str):
                role = OrgRole(role)

            account = add_existing_user_to_org(
                db,
                user_id=str(existing_user.id),
                organization_id=organization_id,
                role=role,
            )
        else:
            account = create_org_member_directly(db, **user_data)

    else:
        # For non-org_member accounts, check for duplicates across all account types
        if (
            get_user_by_email(db, email)
            or get_organization_by_email(db, email)
            or get_admin_by_email(db, email)
            or get_org_member_by_email(db, email)
        ):
            raise UserAlreadyExistsException(
                "An account with this email already exists"
            )

        if account_type == "organization":
            account = create_organization_with_email(db, **user_data)
        elif account_type == "user":
            account = create_user(db, **user_data)
        elif account_type == "admin":
            account = create_admin(db, **user_data)
        else:
            raise ValueError(
                "Invalid account_type. Must be 'user', 'organization', 'org_member' or 'admin'."
            )

    # Generate access and refresh tokens
    token_sub = str(account.id)
    access_token = create_access_token(data={"sub": token_sub})
    refresh_token = create_refresh_token(data={"sub": token_sub})

    schema_account = to_schema(account)

    return AuthenticatedUserOut(
        user=schema_account,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


def register_user_service_with_response(
    db: Session,
    user_data: dict,
    client_type_raw: str,
    account_type: Literal["user", "organization", "admin", "org_member"] = "user",
):
    """Sign up service for all user type"""
    client_type: ClientType = validate_client_type(client_type_raw)
    auth_out = register_account(db, user_data, account_type)

    if client_type == "web":
        return {
            "user": auth_out.user,
            "access_token": auth_out.access_token,
            "refresh_token": auth_out.refresh_token,
            "token_type": auth_out.token_type,
            "set_cookies": True,
        }
    # For mobile, no cookie setting needed
    return {
        "user": auth_out.user,
        "access_token": auth_out.access_token,
        "refresh_token": auth_out.refresh_token,
        "token_type": auth_out.token_type,
        "set_cookies": False,
    }


def check_auth(
    user_obj: Union[User, OrgMember, Organization, Admin, None],
    password: str,
    context: str,
):
    """Shared authentication user login across user types"""
    if not user_obj:
        raise UserNotFoundException(f"{context.capitalize()} not found")
    if not isinstance(user_obj.hashed_password, str) or not verify_password(
        password, user_obj.hashed_password
    ):
        raise PasswordException(f"Invalid password for {context}")


def authenticate_by_context(
    db: Session,
    email: str,
    password: str,
    login_context: Literal["user", "organization", "admin", "org_member"] = "user",
) -> tuple[Union[User, OrgMember, Organization, Admin], UserType, str, str]:
    """Authenticate User type"""

    normalized_email = email.strip().lower()

    if login_context == "org_member":
        org_member = get_org_member_by_email(db, normalized_email)
        if not org_member:
            raise UserNotFoundException("Organization member not found")
        check_auth(org_member, password, context="org_member")
        if org_member.role is None:
            raise UserNotFoundException("Organization member role not found")
        return (org_member, UserType.ORG_MEMBER, str(org_member.role), "bearer")

    if login_context == "organization":
        org = get_organization_by_email(db, normalized_email)
        if not org:
            raise UserNotFoundException("Organization not found")
        check_auth(org, password, context="organization")
        return org, UserType.ORGANIZATION, "org_admin", "bearer"

    if login_context == "admin":
        admin = get_admin_by_email(db, normalized_email)
        if not admin:
            raise UserNotFoundException("Admin not found")
        check_auth(admin, password, context="admin")
        return admin, UserType.ADMIN, "admin", "bearer"

    user = get_user_by_email(db, normalized_email)
    check_auth(user, password, context="user")

    if user is not None and str(user.user_type) == UserType.ADMIN.value:
        return user, UserType.ADMIN, "admin", "bearer"

    return user, UserType.USER, "user", "bearer"


def login_user_service_with_response(
    db: Session,
    email: str,
    password: str,
    client_type_raw: str,
    login_context: Literal["user", "organization", "admin", "org_member"] = "user",
):
    """Login service for all user type"""
    client_type: ClientType = validate_client_type(client_type_raw)
    user, user_type, role, token_type = authenticate_by_context(
        db, email, password, login_context
    )

    tokens = {
        "access_token": create_access_token(data={"sub": str(user.id)}),
        "refresh_token": create_refresh_token(data={"sub": str(user.id)}),
        "token_type": token_type,
    }

    response = {
        "user": to_schema(user),
        **tokens,
        "user_type": user_type,
        "role": role,
        "set_cookies": client_type == "web",
    }

    if client_type == "web":
        response["access_token"] = None
        response["refresh_token"] = None

    return response
