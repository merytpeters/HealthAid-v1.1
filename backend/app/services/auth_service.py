"""User Service: Handles business logic"""
from typing import Literal, Union
from sqlalchemy.orm import Session
from backend.app.models.user import (
    User,
    OrgMember,
    UserType,
    Organization,
    Admin
)
from backend.app.crud import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_org_member_by_email,
    get_organization_by_email,
    create_organization_with_email,
    create_admin,
    get_admin_by_email
)
from backend.lib.utils.user import (
    create_access_token,
    verify_password,
    is_strong_password,
    get_current_user,
    create_refresh_token
)
from backend.lib.utils.clienttype import ClientType, validate_client_type
from backend.lib.errorlib.auth import (
    WeakPasswordException,
    PasswordException,
    UserNotAuthorizedException,
    TokenException,
    UserAlreadyExistsException,
    UserNotFoundException
)
from backend.app.schemas.user.user import UserOut, AuthenticatedUserOut
from backend.app.schemas.org import OrgMemberOut, OrganizationOut
from backend.app.schemas.admin import AdminOut


MODEL_TO_SCHEMA = {
    "User": UserOut,
    "OrgMember": OrgMemberOut,
    "Admin": AdminOut,
    "Organization": OrganizationOut
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
    account_type: Literal["user", "organization", "admin"]
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

    # Check for duplicates across users and organizations
    if (
        get_user_by_email(db, email)
        or get_organization_by_email(db, email)
        or get_admin_by_email(db, email)
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
            "Invalid account_type. Must be 'user', 'organization' or 'admin'."
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
        token_type="bearer"
    )


def register_user_service_with_response(
    db: Session,
    user_data: dict,
    client_type_raw: str,
    account_type: Literal["user", "organization", "admin"] = "user"
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
    context: str
):
    """Shared authentication user login across user types"""
    if not user_obj:
        raise UserNotFoundException(f"{context.capitalize()} not found")
    if not isinstance(
        user_obj.hashed_password,
        str
    ) or not verify_password(
        password,
        user_obj.hashed_password
    ):
        raise PasswordException(f"Invalid password for {context}")


def authenticate_by_context(
    db: Session,
    email: str,
    password: str,
    login_context: Literal["user", "organization", "admin"] = "user"
) -> tuple[Union[User, OrgMember, Organization, Admin], UserType, str, str]:
    """Authenticate User type"""

    normalized_email = email.strip().lower()

    if login_context == "organization":
        org_member = get_org_member_by_email(db, normalized_email)
        if org_member:
            check_auth(org_member, password, context="organization")
            if org_member.role is None:
                raise UserNotFoundException(
                    "Organization member role not found"
                )
            return (
                org_member,
                UserType.ORGANIZATION,
                str(org_member.role),
                "bearer"
            )

        org = get_organization_by_email(db, normalized_email)
        if org:
            check_auth(org, password, context="organization")
            return org, UserType.ORGANIZATION, "org_admin", "bearer"

        raise UserNotFoundException(
            "No OrgMember or Organization with this email"
        )

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
    login_context: Literal["user", "organization", "admin"] = "user"
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


def get_current_user_from_db(token: str, db: Session) -> tuple[User, str]:
    """Fetch the current user from the db using the provided user data."""
    credentials_exception = TokenException(401, "Invalid or expired token.")
    user_exception = UserNotAuthorizedException()

    if not isinstance(token, str) or not token:
        raise credentials_exception
    user = get_current_user(token, credentials_exception)
    db_user = get_user_by_id(db, user["id"])

    if not db_user:
        raise user_exception

    return db_user, str(db_user.email)
