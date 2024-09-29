import httpx
from typing import Any, Dict


class BaseHttpService:
    __slots__ = ("base_url", "api_key")

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    async def _get(self, endpoint: str, params: Dict[str, Any] = None) -> httpx.Response:
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}{endpoint}", params=params)
            return response

    async def _post(self, endpoint: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> httpx.Response:
        if headers is None:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data['apiKey'] = self.api_key
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}{endpoint}", data=data, headers=headers)
            return response
