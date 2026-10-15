from __future__ import annotations
from typing import TYPE_CHECKING, Any, AsyncIterator, Iterator, List, Optional

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.base import PaginatedList
from ..models.contacts import Contact
from ._common import search_path

class ContactsAPI:
    """Synchronous implementation of the Contacts API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create(self, **kwargs: Any) -> Contact:
        """Create a new contact."""
        res = self._client.request("POST", "contacts", json=kwargs)
        return Contact.model_validate(res)

    def view(self, id: int) -> Contact:
        """View a contact by ID."""
        res = self._client.request("GET", f"contacts/{id}")
        return Contact.model_validate(res)

    def list(self, **kwargs: Any) -> List[Contact]:
        """List all contacts."""
        res = self._client.request("GET", "contacts", params=kwargs)
        return [Contact.model_validate(c) for c in res]

    def iter_all(self, **kwargs: Any) -> Iterator[Contact]:
        """Iterate over all contacts, fetching pages lazily (see ``list`` for filters)."""
        return self._client.paginate("contacts", Contact, kwargs)
        
    def filter(
        self, query: str, page: Optional[int] = None
    ) -> PaginatedList[Contact]:
        """Filter contacts with a Freshdesk query, e.g. ``"status:2 AND priority:3"``.

        The query is wrapped in double quotes unless it already is.  Each
        page holds 30 results; *page* can be 1-10.  ``total`` is the full
        match count.
        """
        res = self._client.request("GET", search_path("contacts", query, page))
        return PaginatedList[Contact](
            items=res.get("results", []), total=res.get("total")
        )
        
    def search(self, term: str) -> List[Contact]:
        """Search contacts by term."""
        res = self._client.request("GET", "contacts/autocomplete", params={"term": term})
        return [Contact.model_validate(c) for c in res]

    def update(self, id: int, **kwargs: Any) -> Contact:
        """Update a contact."""
        res = self._client.request("PUT", f"contacts/{id}", json=kwargs)
        return Contact.model_validate(res)

    def delete(self, id: int) -> None:
        """Soft delete a contact."""
        self._client.request("DELETE", f"contacts/{id}")

    def hard_delete(self, id: int) -> None:
        """Permanently delete a contact."""
        self._client.request("DELETE", f"contacts/{id}/hard_delete")

    def restore(self, id: int) -> None:
        """Restore a soft deleted contact."""
        self._client.request("PUT", f"contacts/{id}/restore")

    def make_agent(self, id: int, **kwargs: Any) -> Any:
        """Convert a contact into an agent."""
        return self._client.request("PUT", f"contacts/{id}/make_agent", json=kwargs)

    def send_invite(self, id: int) -> None:
        """Send an activation URL to the contact."""
        self._client.request("PUT", f"contacts/{id}/send_invite")

    def merge(self, primary_contact_id: int, secondary_contact_ids: List[int]) -> Any:
        """Merge a set of secondary contacts into a primary contact."""
        payload = {
            "primary_contact_id": primary_contact_id,
            "secondary_contact_ids": secondary_contact_ids
        }
        return self._client.request("PUT", "contacts/merge", json=payload)


class AsyncContactsAPI:
    """Asynchronous implementation of the Contacts API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def create(self, **kwargs: Any) -> Contact:
        """Create a new contact."""
        res = await self._client.request("POST", "contacts", json=kwargs)
        return Contact.model_validate(res)

    async def view(self, id: int) -> Contact:
        """View a contact by ID."""
        res = await self._client.request("GET", f"contacts/{id}")
        return Contact.model_validate(res)

    async def list(self, **kwargs: Any) -> List[Contact]:
        """List all contacts."""
        res = await self._client.request("GET", "contacts", params=kwargs)
        return [Contact.model_validate(c) for c in res]

    def iter_all(self, **kwargs: Any) -> AsyncIterator[Contact]:
        """Iterate over all contacts, fetching pages lazily (see ``list`` for filters)."""
        return self._client.paginate("contacts", Contact, kwargs)
        
    async def filter(
        self, query: str, page: Optional[int] = None
    ) -> PaginatedList[Contact]:
        """Filter contacts with a Freshdesk query, e.g. ``"status:2 AND priority:3"``.

        The query is wrapped in double quotes unless it already is.  Each
        page holds 30 results; *page* can be 1-10.  ``total`` is the full
        match count.
        """
        res = await self._client.request("GET", search_path("contacts", query, page))
        return PaginatedList[Contact](
            items=res.get("results", []), total=res.get("total")
        )
        
    async def search(self, term: str) -> List[Contact]:
        """Search contacts by term."""
        res = await self._client.request("GET", "contacts/autocomplete", params={"term": term})
        return [Contact.model_validate(c) for c in res]

    async def update(self, id: int, **kwargs: Any) -> Contact:
        """Update a contact."""
        res = await self._client.request("PUT", f"contacts/{id}", json=kwargs)
        return Contact.model_validate(res)

    async def delete(self, id: int) -> None:
        """Soft delete a contact."""
        await self._client.request("DELETE", f"contacts/{id}")

    async def hard_delete(self, id: int) -> None:
        """Permanently delete a contact."""
        await self._client.request("DELETE", f"contacts/{id}/hard_delete")

    async def restore(self, id: int) -> None:
        """Restore a soft deleted contact."""
        await self._client.request("PUT", f"contacts/{id}/restore")

    async def make_agent(self, id: int, **kwargs: Any) -> Any:
        """Convert a contact into an agent."""
        return await self._client.request("PUT", f"contacts/{id}/make_agent", json=kwargs)

    async def send_invite(self, id: int) -> None:
        """Send an activation URL to the contact."""
        await self._client.request("PUT", f"contacts/{id}/send_invite")

    async def merge(self, primary_contact_id: int, secondary_contact_ids: List[int]) -> Any:
        """Merge a set of secondary contacts into a primary contact."""
        payload = {
            "primary_contact_id": primary_contact_id,
            "secondary_contact_ids": secondary_contact_ids
        }
        return await self._client.request("PUT", "contacts/merge", json=payload)
