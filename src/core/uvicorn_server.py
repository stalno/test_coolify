import uvicorn

from typing import Any
from src.core.settings import Settings


def run_api_uvicorn(app: Any, config: Settings, **kwargs: Any) -> None:
    uv_config = uvicorn.Config(
        app,
        host=config.server.host,
        port=config.server.port,
        server_header=False,
        **kwargs,
    )
    server = uvicorn.Server(uv_config)
    server.run()
