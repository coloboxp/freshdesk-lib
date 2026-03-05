from __future__ import annotations
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.groups import Group

class GroupsAPI:
    """Synchronous implementation of the Groups API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create(self, **kwargs: Any) -> Group:
        """Create a new group."""
        res = self._client.request("POST", "groups", json=kwargs)
        return Group.model_validate(res)

    def view(self, id: int) -> Group:
        """View a group by ID."""
        res = self._client.request("GET", f"groups/{id}")
        return Group.model_validate(res)

    def list(self, **kwargs: Any) -> List[Group]:
        """List all groups."""
        res = self._client.request("GET", "groups", params=kwargs)
        return [Group.model_validate(c) for c in res]

    def update(self, id: int, **kwargs: Any) -> Group:
        """Update a group."""
        res = self._client.request("PUT", f"groups/{id}", json=kwargs)
        return Group.model_validate(res)

    def delete(self, id: int) -> None:
        """Delete a group."""
        self._client.request("DELETE", f"groups/{id}")


class AsyncGroupsAPI:
    """Asynchronous implementation of the Groups API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def create(self, **kwargs: Any) -> Group:
        """Create a new group."""
        res = await self._client.request("POST", "groups", json=kwargs)
        return Group.model_validate(res)

    async def view(self, id: int) -> Group:
        """View a group by ID."""
        res = await self._client.request("GET", f"groups/{id}")
        return Group.model_validate(res)

    async def list(self, **kwargs: Any) -> List[Group]:
        """List all groups."""
        res = await self._client.request("GET", "groups", params=kwargs)
        return [Group.model_validate(c) for c in res]

    async def update(self, id: int, **kwargs: Any) -> Group:
        """Update a group."""
        res = await self._client.request("PUT", f"groups/{id}", json=kwargs)
        return Group.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete a group."""
        await self._client.request("DELETE", f"groups/{id}")
