from __future__ import annotations
from typing import TYPE_CHECKING, Any, AsyncIterator, Iterator, List, Optional, Sequence

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.base import PaginatedList
from ..models.tickets import Ticket
from ._common import AttachmentInput, body_kwargs, search_path

class TicketsAPI:
    """Synchronous implementation of the Tickets API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create(
        self, attachments: Optional[Sequence[AttachmentInput]] = None, **kwargs: Any
    ) -> Ticket:
        """Create a new ticket.  *attachments* switches to a multipart upload."""
        res = self._client.request(
            "POST", "tickets", **body_kwargs(kwargs, attachments)
        )
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

    def iter_all(self, **kwargs: Any) -> Iterator[Ticket]:
        """Iterate over all tickets, fetching pages lazily (see ``list`` for filters)."""
        return self._client.paginate("tickets", Ticket, kwargs)
        
    def filter(
        self, query: str, page: Optional[int] = None
    ) -> PaginatedList[Ticket]:
        """Filter tickets with a Freshdesk query, e.g. ``"status:2 AND priority:3"``.

        The query is wrapped in double quotes unless it already is.  Each
        page holds 30 results; *page* can be 1-10.  ``total`` is the full
        match count.
        """
        res = self._client.request("GET", search_path("tickets", query, page))
        return PaginatedList[Ticket](
            items=res.get("results", []), total=res.get("total")
        )

    def update(
        self,
        id: int,
        attachments: Optional[Sequence[AttachmentInput]] = None,
        **kwargs: Any,
    ) -> Ticket:
        """Update a ticket.  *attachments* switches to a multipart upload."""
        res = self._client.request(
            "PUT", f"tickets/{id}", **body_kwargs(kwargs, attachments)
        )
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

    async def create(
        self, attachments: Optional[Sequence[AttachmentInput]] = None, **kwargs: Any
    ) -> Ticket:
        """Create a new ticket.  *attachments* switches to a multipart upload."""
        res = await self._client.request(
            "POST", "tickets", **body_kwargs(kwargs, attachments)
        )
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

    def iter_all(self, **kwargs: Any) -> AsyncIterator[Ticket]:
        """Iterate over all tickets, fetching pages lazily (see ``list`` for filters)."""
        return self._client.paginate("tickets", Ticket, kwargs)
        
    async def filter(
        self, query: str, page: Optional[int] = None
    ) -> PaginatedList[Ticket]:
        """Filter tickets with a Freshdesk query, e.g. ``"status:2 AND priority:3"``.

        The query is wrapped in double quotes unless it already is.  Each
        page holds 30 results; *page* can be 1-10.  ``total`` is the full
        match count.
        """
        res = await self._client.request("GET", search_path("tickets", query, page))
        return PaginatedList[Ticket](
            items=res.get("results", []), total=res.get("total")
        )

    async def update(
        self,
        id: int,
        attachments: Optional[Sequence[AttachmentInput]] = None,
        **kwargs: Any,
    ) -> Ticket:
        """Update a ticket.  *attachments* switches to a multipart upload."""
        res = await self._client.request(
            "PUT", f"tickets/{id}", **body_kwargs(kwargs, attachments)
        )
        return Ticket.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete a ticket."""
        await self._client.request("DELETE", f"tickets/{id}")

    async def restore(self, id: int) -> None:
        """Restore a deleted ticket."""
        await self._client.request("PUT", f"tickets/{id}/restore")

    async def forward(self, id: int, **kwargs: Any) -> Any:
        await self._client.request("POST", f"tickets/{id}/forward", json=kwargs)
