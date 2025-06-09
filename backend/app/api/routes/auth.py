"""Authorization and authentication APIs"""
from sqlalchemy.orm import Session
from backend.lib.crud import create_user
from fastapi import APIRouter, Depends, status
from backend.app.schemas.user import UserCreate, UserOut
from backend.app.db.session import get_db 


router = APIRouter(prefix="/auth")

"""Regular User API"""
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """Register a regular/single user"""
    user = create_user(db, user_create)
    return user
    
"""Admin API"""


"""Org API"""


"""Org Staff API"""