from app.api.v1.auth.crud import get_user_by_id, get_user_by_id_and_type
from lib.utils.user import get_current_user
from lib.errorlib.auth import (
    UserNotAuthorizedException,
    TokenException,
)
from app.api.v1.auth.models.user import User
from sqlalchemy.orm import Session


def get_current_user_from_db(token: str, db: Session) -> tuple[User, str]:
    """Fetch the current user from the db using the provided user data."""
    credentials_exception = TokenException(401, "Invalid or expired token.")
    user_exception = UserNotAuthorizedException()

    if not isinstance(token, str) or not token:
        raise credentials_exception
    user_data = get_current_user(token, credentials_exception)
    user_id = user_data["id"]
    user_type = user_data.get("user_type")

    if user_type:
        db_user = get_user_by_id_and_type(db, user_id, user_type)
    else:
        db_user = get_user_by_id(db, user_id)

    if not db_user:
        raise user_exception

    return db_user, str(db_user.email)
