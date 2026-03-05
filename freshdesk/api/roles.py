from __future__ import annotations
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.roles import Role

class RolesAPI:
    """Synchronous implementation of the Roles API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def view(self, id: int) -> Role:
        """View a role by ID."""
        res = self._client.request("GET", f"roles/{id}")
        return Role.model_validate(res)

    def list(self, **kwargs: Any) -> List[Role]:
        """List all roles."""
        res = self._client.request("GET", "roles", params=kwargs)
        return [Role.model_validate(r) for r in res]


class AsyncRolesAPI:
    """Asynchronous implementation of the Roles API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def view(self, id: int) -> Role:
        """View a role by ID."""
        res = await self._client.request("GET", f"roles/{id}")
        return Role.model_validate(res)

    async def list(self, **kwargs: Any) -> List[Role]:
        """List all roles."""
        res = await self._client.request("GET", "roles", params=kwargs)
        return [Role.model_validate(r) for r in res]
