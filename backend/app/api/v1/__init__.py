from fastapi import APIRouter
from backend.app.api.v1.auth.routes.auth import router as auth_router
from backend.app.api.v1.auth.routes.user.profile import router as user_profile_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(user_profile_router)
