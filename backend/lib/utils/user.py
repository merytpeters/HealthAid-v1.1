"""Utility functions for handling JWT tokens."""

import os
from datetime import datetime, timedelta
import uuid
import bcrypt
import redis
from jose import JWTError, jwt
from fastapi import Response


SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


redis_client = redis.Redis(host="localhost", port=6379, db=0)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with an expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire.timestamp(), "jti": jti})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a jwt refresh token with an expiration"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire.timestamp(), "jti": jti})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def blacklist_token(jti: str, expires_in_seconds: int):
    """Blacklist token"""
    redis_client.setex(jti, expires_in_seconds, "true")


def is_token_blacklisted(jti: str) -> bool:
    """Check if token is blacklisted"""
    return redis_client.exists(jti) == 1


def verify_access_token(token: str, credentials_exception: Exception) -> dict:
    """Verify the JWT access token, reject it if
    blacklisted and return the payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        if jti is not None and is_token_blacklisted(jti):
            raise credentials_exception
        return payload
    except JWTError as exc:
        raise credentials_exception from exc


def delete_auth_cookies(response: Response):
    """Delete Cookies Function For Logout"""
    response.delete_cookie("access_token")
    response.delete_cookie("reefresh_token")


def get_current_user(token: str, credentials_exception: Exception) -> dict:
    """Get the current user from the JWT token."""
    payload = verify_access_token(token, credentials_exception)
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    return {"user_id": user_id}


def token_refresh(refresh_token: str, credentials_exception: Exception) -> str:
    """Refresh the JWT access token if the refresh token is valid."""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        if jti is not None and is_token_blacklisted(jti):
            raise credentials_exception
        if payload.get("exp") is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception

    new_access_token = create_access_token(data={"sub": user_id})
    return new_access_token


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


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
