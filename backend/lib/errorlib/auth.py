"""Error handling module for user-related operations in FastAPI.
This module defines custom exceptions for various user-related errors,
such as invalid credentials, user already exists, user not found
"""
from fastapi import HTTPException, status


class InvalidCredentialsException(HTTPException):
    """Exception raised for invalid user credentials."""
    def __init__(self, detail: str = "Invalid email or password."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail
        )


class UserAlreadyExistsException(HTTPException):
    """Exception raised when a user with the given email or
    username already exists."""

    def __init__(
        self, detail: str = "User with this email or username already exists."
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class UserNotFoundException(HTTPException):
    """Exception raised when a user is not found in the database."""
    def __init__(self, detail: str = "User not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail
        )


class UserNotAuthorizedException(HTTPException):
    """Exception raised when a user is not authorized to perform an action."""
    def __init__(
        self, detail: str = "User is not authorized to perform this action."
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail
        )


class TokenException(HTTPException):
    """Exception raised for token-related errors."""
    def __init__(
        self, detail: str = "Token error.",
        status_code=status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(
            status_code=status_code, detail=detail
        )


class PasswordException(HTTPException):
    """Exception raised for password-related errors."""
    def __init__(self, detail: str = "Password error."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class EmailException(HTTPException):
    """Exception raised for email-related errors."""
    def __init__(self, detail: str = "Email error."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class UserOperationException(HTTPException):
    """Exception raised for general user operation errors."""
    def __init__(self, detail: str = "User operation failed."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class DBIntegrityException(HTTPException):
    """Exception raised for database integrity errors."""
    def __init__(self, detail: str = "Database integrity error."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class DBInitializationException(HTTPException):
    """Exception raised for database initialization errors."""
    def __init__(self, detail: str = "Database initialization error."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class DBOperationException(HTTPException):
    """Exception raised for database operation errors."""
    def __init__(self, detail: str = "Database operation error."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class DBConnectionException(HTTPException):
    """Exception raised for database connection errors."""
    def __init__(self, detail: str = "Database connection error."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class DBQueryException(HTTPException):
    """Exception raised for database query errors."""
    def __init__(self, detail: str = "Database query error."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class DBSessionException(HTTPException):
    """Exception raised for database session errors."""
    def __init__(self, detail: str = "Database session error."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class WeakPasswordException(HTTPException):
    """Exception for weak password"""
    def __init__(self, detail: str = "Password is too weak"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )
