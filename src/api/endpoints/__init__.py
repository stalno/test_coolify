from fastapi import APIRouter, FastAPI

from src.api.endpoints.user import user_router
from src.api.endpoints.api import api_router

router = APIRouter()

router.include_router(user_router)
router.include_router(api_router)


def setup_routers(app: FastAPI) -> None:
    app.include_router(router)
