import httpx
from typing import Any, Dict, List, Optional
import urllib.parse

class FrappeClient:
    def __init__(self, url: str, token: str, timeout: float = 30.0):
        self.url = url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _get_api_url(self, method: str) -> str:
        return f"{self.url}/api/method/mcp_server.api.{method}"

    async def _post(self, method: str, data: Optional[Dict[str, Any]] = None) -> Any:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._get_api_url(method),
                    json=data or {},
                    headers=self.headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                result = response.json()
                
                if "message" in result:
                    return result["message"]
                return result
            except httpx.HTTPStatusError as e:
                try:
                    error_details = e.response.json()
                    raise Exception(f"Frappe API Error: {error_details.get('_server_messages', str(e))}")
                except Exception:
                    raise Exception(f"HTTP Error: {str(e)}")
            except httpx.RequestError as e:
                raise Exception(f"Connection Error: {str(e)}")

    async def search_docs(
        self, 
        doctype: str, 
        filters: Optional[Dict[str, Any]] = None,
        fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        payload = {
            "doctype": doctype,
            "filters": filters,
            "fields": fields
        }
        return await self._post("search_docs", payload)

    async def create_doc(self, doctype: str, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "doctype": doctype,
            "data": data
        }
        return await self._post("create_doc", payload)

    async def update_doc(self, doctype: str, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "doctype": doctype,
            "name": name,
            "data": data
        }
        return await self._post("update_doc", payload)

    async def get_doc(self, doctype: str, name: str) -> Dict[str, Any]:
        payload = {
            "doctype": doctype,
            "name": name
        }
        return await self._post("get_doc", payload)

    async def get_meta(self, doctype: str) -> Dict[str, Any]:
        payload = {
            "doctype": doctype
        }
        return await self._post("get_meta", payload)

    async def delete_doc(self, doctype: str, name: str) -> Dict[str, Any]:
        payload = {
            "doctype": doctype,
            "name": name
        }
        return await self._post("delete_doc", payload)

    async def ping(self) -> Dict[str, Any]:
        return await self._post("ping")
