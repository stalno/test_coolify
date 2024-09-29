from typing import Any, Generic, Mapping, Optional

from fastapi.responses import JSONResponse as _JSONResponse
from starlette.background import BackgroundTask
import httpx
import json

from typing import TypeVar


ResultType = TypeVar("ResultType")


class JSONResponse(_JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(content).encode()


class OkResponse(JSONResponse, Generic[ResultType]):
    __slots__ = ()

    def __init__(
        self,
        content: ResultType,
        status_code: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[BackgroundTask] = None,
    ) -> None:
        if isinstance(content, dict) and 'status_code' in content:
            status_code = content["status_code"]
        super().__init__(content, status_code, headers, media_type, background)
