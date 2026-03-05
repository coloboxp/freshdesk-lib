from __future__ import annotations
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.canned_responses import CannedResponse, CannedResponseFolder

class CannedResponsesAPI:
    """Synchronous implementation of the Canned Responses API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Canned Responses
    def create(self, **kwargs: Any) -> CannedResponse:
        """Create a canned response."""
        res = self._client.request("POST", "canned_responses", json=kwargs)
        return CannedResponse.model_validate(res)

    def view(self, id: int) -> CannedResponse:
        """View a canned response by ID."""
        res = self._client.request("GET", f"canned_responses/{id}")
        return CannedResponse.model_validate(res)

    def update(self, id: int, **kwargs: Any) -> CannedResponse:
        """Update a canned response."""
        res = self._client.request("PUT", f"canned_responses/{id}", json=kwargs)
        return CannedResponse.model_validate(res)

    def delete(self, id: int) -> None:
        """Delete a canned response."""
        self._client.request("DELETE", f"canned_responses/{id}")

    # Folders
    def create_folder(self, **kwargs: Any) -> CannedResponseFolder:
        """Create a canned response folder."""
        res = self._client.request("POST", "canned_response_folders", json=kwargs)
        return CannedResponseFolder.model_validate(res)

    def update_folder(self, id: int, **kwargs: Any) -> CannedResponseFolder:
        """Update a canned response folder."""
        res = self._client.request("PUT", f"canned_response_folders/{id}", json=kwargs)
        return CannedResponseFolder.model_validate(res)

    def delete_folder(self, id: int) -> None:
        """Delete a canned response folder."""
        self._client.request("DELETE", f"canned_response_folders/{id}")

    def list_folders(self) -> List[CannedResponseFolder]:
        """List all canned response folders."""
        res = self._client.request("GET", "canned_response_folders")
        return [CannedResponseFolder.model_validate(f) for f in res]

    def list_responses_in_folder(self, folder_id: int) -> List[CannedResponse]:
        """List all canned responses in a folder."""
        res = self._client.request("GET", f"canned_response_folders/{folder_id}/responses")
        return [CannedResponse.model_validate(r) for r in res]


class AsyncCannedResponsesAPI:
    """Asynchronous implementation of the Canned Responses API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Canned Responses
    async def create(self, **kwargs: Any) -> CannedResponse:
        """Create a canned response."""
        res = await self._client.request("POST", "canned_responses", json=kwargs)
        return CannedResponse.model_validate(res)

    async def view(self, id: int) -> CannedResponse:
        """View a canned response by ID."""
        res = await self._client.request("GET", f"canned_responses/{id}")
        return CannedResponse.model_validate(res)

    async def update(self, id: int, **kwargs: Any) -> CannedResponse:
        """Update a canned response."""
        res = await self._client.request("PUT", f"canned_responses/{id}", json=kwargs)
        return CannedResponse.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete a canned response."""
        await self._client.request("DELETE", f"canned_responses/{id}")

    # Folders
    async def create_folder(self, **kwargs: Any) -> CannedResponseFolder:
        """Create a canned response folder."""
        res = await self._client.request("POST", "canned_response_folders", json=kwargs)
        return CannedResponseFolder.model_validate(res)

    async def update_folder(self, id: int, **kwargs: Any) -> CannedResponseFolder:
        """Update a canned response folder."""
        res = await self._client.request("PUT", f"canned_response_folders/{id}", json=kwargs)
        return CannedResponseFolder.model_validate(res)

    async def delete_folder(self, id: int) -> None:
        """Delete a canned response folder."""
        await self._client.request("DELETE", f"canned_response_folders/{id}")

    async def list_folders(self) -> List[CannedResponseFolder]:
        """List all canned response folders."""
        res = await self._client.request("GET", "canned_response_folders")
        return [CannedResponseFolder.model_validate(f) for f in res]

    async def list_responses_in_folder(self, folder_id: int) -> List[CannedResponse]:
        """List all canned responses in a folder."""
        res = await self._client.request("GET", f"canned_response_folders/{folder_id}/responses")
        return [CannedResponse.model_validate(r) for r in res]
