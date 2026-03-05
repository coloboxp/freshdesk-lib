from __future__ import annotations
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.tickets import Ticket

class TicketsAPI:
    """Synchronous implementation of the Tickets API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create(self, **kwargs: Any) -> Ticket:
        """Create a new ticket."""
        res = self._client.request("POST", "tickets", json=kwargs)
        return Ticket.model_validate(res)

    def view(self, id: int, include: Optional[str] = None) -> Ticket:
        """View a ticket by ID."""
        params = {"include": include} if include else None
        res = self._client.request("GET", f"tickets/{id}", params=params)
        return Ticket.model_validate(res)

    def list(self, **kwargs: Any) -> List[Ticket]:
        """List all tickets."""
        res = self._client.request("GET", "tickets", params=kwargs)
        return [Ticket.model_validate(t) for t in res]
        
    def filter(self, query: str) -> List[Ticket]:
        """Filter tickets using a query string."""
        res = self._client.request("GET", "search/tickets", params={"query": query})
        return [Ticket.model_validate(t) for t in res.get("results", [])]

    def update(self, id: int, **kwargs: Any) -> Ticket:
        """Update a ticket."""
        res = self._client.request("PUT", f"tickets/{id}", json=kwargs)
        return Ticket.model_validate(res)

    def delete(self, id: int) -> None:
        """Delete a ticket."""
        self._client.request("DELETE", f"tickets/{id}")

    def restore(self, id: int) -> None:
        """Restore a deleted ticket."""
        self._client.request("PUT", f"tickets/{id}/restore")

    def forward(self, id: int, **kwargs: Any) -> Any:
        self._client.request("POST", f"tickets/{id}/forward", json=kwargs)


class AsyncTicketsAPI:
    """Asynchronous implementation of the Tickets API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def create(self, **kwargs: Any) -> Ticket:
        """Create a new ticket."""
        res = await self._client.request("POST", "tickets", json=kwargs)
        return Ticket.model_validate(res)

    async def view(self, id: int, include: Optional[str] = None) -> Ticket:
        """View a ticket by ID."""
        params = {"include": include} if include else None
        res = await self._client.request("GET", f"tickets/{id}", params=params)
        return Ticket.model_validate(res)

    async def list(self, **kwargs: Any) -> List[Ticket]:
        """List all tickets."""
        res = await self._client.request("GET", "tickets", params=kwargs)
        return [Ticket.model_validate(t) for t in res]
        
    async def filter(self, query: str) -> List[Ticket]:
        """Filter tickets using a query string."""
        res = await self._client.request("GET", "search/tickets", params={"query": query})
        return [Ticket.model_validate(t) for t in res.get("results", [])]

    async def update(self, id: int, **kwargs: Any) -> Ticket:
        """Update a ticket."""
        res = await self._client.request("PUT", f"tickets/{id}", json=kwargs)
        return Ticket.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete a ticket."""
        await self._client.request("DELETE", f"tickets/{id}")

    async def restore(self, id: int) -> None:
        """Restore a deleted ticket."""
        await self._client.request("PUT", f"tickets/{id}/restore")

    async def forward(self, id: int, **kwargs: Any) -> Any:
        await self._client.request("POST", f"tickets/{id}/forward", json=kwargs)
