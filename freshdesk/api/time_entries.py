from __future__ import annotations
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.time_entries import TimeEntry

class TimeEntriesAPI:
    """Synchronous implementation of the Time Entries API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def list(self, **kwargs: Any) -> List[TimeEntry]:
        """List all time entries."""
        res = self._client.request("GET", "time_entries", params=kwargs)
        return [TimeEntry.model_validate(t) for t in res]

    def create(self, ticket_id: int, **kwargs: Any) -> TimeEntry:
        """Create a time entry for a ticket."""
        res = self._client.request("POST", f"tickets/{ticket_id}/time_entries", json=kwargs)
        return TimeEntry.model_validate(res)

    def update(self, id: int, **kwargs: Any) -> TimeEntry:
        """Update a time entry."""
        res = self._client.request("PUT", f"time_entries/{id}", json=kwargs)
        return TimeEntry.model_validate(res)

    def toggle_timer(self, id: int) -> TimeEntry:
        """Start/Stop timer for a time entry."""
        res = self._client.request("PUT", f"time_entries/{id}/toggle_timer")
        return TimeEntry.model_validate(res)

    def delete(self, id: int) -> None:
        """Delete a time entry."""
        self._client.request("DELETE", f"time_entries/{id}")


class AsyncTimeEntriesAPI:
    """Asynchronous implementation of the Time Entries API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def list(self, **kwargs: Any) -> List[TimeEntry]:
        """List all time entries."""
        res = await self._client.request("GET", "time_entries", params=kwargs)
        return [TimeEntry.model_validate(t) for t in res]

    async def create(self, ticket_id: int, **kwargs: Any) -> TimeEntry:
        """Create a time entry for a ticket."""
        res = await self._client.request("POST", f"tickets/{ticket_id}/time_entries", json=kwargs)
        return TimeEntry.model_validate(res)

    async def update(self, id: int, **kwargs: Any) -> TimeEntry:
        """Update a time entry."""
        res = await self._client.request("PUT", f"time_entries/{id}", json=kwargs)
        return TimeEntry.model_validate(res)

    async def toggle_timer(self, id: int) -> TimeEntry:
        """Start/Stop timer for a time entry."""
        res = await self._client.request("PUT", f"time_entries/{id}/toggle_timer")
        return TimeEntry.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete a time entry."""
        await self._client.request("DELETE", f"time_entries/{id}")
