"""Authorization and authentication APIs"""
from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Request,
    HTTPException
)
from sqlalchemy.orm import Session
from backend.app.schemas.user import (
    UserCreate,
    AuthenticatedUserOut,
    UserLogin,
)
from backend.app.db.session import get_db
from backend.lib.errorlib.auth import (
    UserNotFoundException,
    PasswordException
)
from backend.app.services.user_service import (
    register_user_service_with_response as register_user_service
)
from backend.app.services.user_service import (
    login_user_service_with_response as login_user_service
)


router = APIRouter()
"""Regular User API"""


@router.post(
    "/register",
    response_model=AuthenticatedUserOut,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_create: UserCreate,
    response: Response,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register regular user"""
    client_type = request.headers.get("X-Client-Type", "web")

    result = register_user_service(
        db,
        user_create.model_dump(exclude_unset=True),
        client_type
    )

    if result["set_cookies"]:
        response.set_cookie(
            "access_token",
            result["access_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age= 15 * 60
        )
        response.set_cookie(
            "refresh_token",
            result["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )

        # Return without tokens in JSON since they are in cookies
        return {
            "user": result["user"],
            "access_token": None,
            "refresh_token": None,
            "token_type": result["token_type"]
        }

    else:
        # Return full response with tokens in JSON
        return {
            "user": result["user"],
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": result["token_type"],
        }


@router.post(
    "/login",
    response_model=AuthenticatedUserOut,
    status_code=status.HTTP_200_OK
)
async def login(
    user_login: UserLogin,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
):
    """Login User"""
    try:
        client_type = request.headers.get("X-Client-Type", "web")

        result = login_user_service(db, user_login.email, user_login.password, client_type)

        if result["set_cookies"]:
            response.set_cookie(
                "access_token",
                result["access_token"],
                httponly=True,
                secure=True,
                samesite="lax",
                max_age= 15 * 60
            )
            response.set_cookie(
                "refresh_token",
                result["refresh_token"],
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=7 * 24 * 60 * 60
            )

            # Return without tokens in JSON since they are in cookies
            return {
                "user": result["user"],
                "access_token": None,
                "refresh_token": None,
                "token_type": result["token_type"]
            }

        else:
            # Return full response with tokens in JSON
            return {
                "user": result["user"],
                "access_token": result["access_token"],
                "refresh_token": result["refresh_token"],
                "token_type": result["token_type"],
            }
    except UserNotFoundException:
        raise HTTPException(status_code=401, detail="User not found")
    except PasswordException:
        raise HTTPException(status_code=401, detail="Invalid credentials")
