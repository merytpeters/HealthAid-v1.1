"""Utility functions for handling JWT tokens."""
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt


SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv(
    "ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    """Create a JWT access token with an expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(
    token: str, credentials_exception: Exception
) -> dict:
    """Verify the JWT access token and return the payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        raise credentials_exception from exc


def get_current_user(token: str, credentials_exception: Exception) -> dict:
    """Get the current user from the JWT token."""
    payload = verify_access_token(token, credentials_exception)
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    return {"user_id": user_id}


def token_refresh(token: str, credentials_exception: Exception) -> str:
    """Refresh the JWT token if it is valid."""
    payload = verify_access_token(token, credentials_exception)
    if payload.get("exp") is None:
        raise credentials_exception
    new_token = create_access_token(data={"sub": payload.get("sub")})
    return new_token

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def is_strong_password(password: str) -> bool:
    """Check if the password is strong enough."""
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isalpha() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password):
        return False
    return True