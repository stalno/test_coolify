from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Any
from src.core.settings import load_settings, Settings
from src.core.uvicorn_server import run_api_uvicorn
from src.api.endpoints import setup_routers


def init_app(settings: Settings, **kwargs: Any) -> FastAPI:
    app = FastAPI(
        default_response_class=JSONResponse,
        docs_url="/docs",
        redoc_url=None,
        swagger_ui_oauth2_redirect_url=None,
        **kwargs,
    )
    setup_routers(app)
    return app


def main() -> None:
    settings = load_settings()  # Загружаем настройки
    app = init_app(settings=settings)  # Инициализируем приложение
    run_api_uvicorn(app, settings)  # Запуск приложения через Uvicorn


if __name__ == "__main__":
    main()
