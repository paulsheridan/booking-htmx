from fastapi import APIRouter

from app.api.routes import users
from app.api.routes import login
from app.api.routes import health_check

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(
    health_check.router, prefix="/health_check", tags=["health_check"]
)