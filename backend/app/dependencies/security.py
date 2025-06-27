"""Auth Security For Protected Routes"""
from fastapi.security import OAuth2PasswordBearer

user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
