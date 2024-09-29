import httpx
from typing import Any, Dict
from src.common.responses.json import OkResponse


class BaseHttpService:
    __slots__ = ("base_url", "api_key")

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    async def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}{endpoint}", params=params)
            if response.status_code != 200:
                return dict(content=response.json(), status_code=response.status_code)
            return response.json()

    async def _post(self, endpoint: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        if headers is None:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data['apiKey'] = self.api_key
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}{endpoint}", data=data, headers=headers)
            if response.status_code != 201:
                return dict(content=response.json(), status_code=response.status_code)
            return response.json()
