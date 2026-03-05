from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.minor_resources import Job, Setting, Thread, ThreadMessage

class MinorResourcesAPI:
    """Synchronous implementation of Minor APIs (Jobs, Settings, Threads)."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Jobs
    def view_job(self, id: str) -> Job:
        """View a job by ID."""
        res = self._client.request("GET", f"jobs/{id}")
        return Job.model_validate(res)

    # Settings
    def view_helpdesk_settings(self) -> Setting:
        """View helpdesk settings."""
        res = self._client.request("GET", "settings/helpdesk")
        return Setting.model_validate(res)

    # Threads
    def create_thread(self, **kwargs: Any) -> Thread:
        """Create a thread."""
        res = self._client.request("POST", "collaboration/threads", json=kwargs)
        return Thread.model_validate(res)

    def get_thread(self, id: int) -> Thread:
        """Get a thread."""
        res = self._client.request("GET", f"collaboration/threads/{id}")
        return Thread.model_validate(res)

    def update_thread(self, id: int, **kwargs: Any) -> Thread:
        """Update a thread."""
        res = self._client.request("PUT", f"collaboration/threads/{id}", json=kwargs)
        return Thread.model_validate(res)

    def delete_thread(self, id: int) -> None:
        """Delete a thread."""
        self._client.request("DELETE", f"collaboration/threads/{id}")

    # Thread messages
    def create_thread_message(self, **kwargs: Any) -> ThreadMessage:
        """Create a message for a thread."""
        res = self._client.request("POST", "collaboration/messages", json=kwargs)
        return ThreadMessage.model_validate(res)

    def get_thread_message(self, id: int) -> ThreadMessage:
        """Get a message from a thread."""
        res = self._client.request("GET", f"collaboration/messages/{id}")
        return ThreadMessage.model_validate(res)

    def update_thread_message(self, id: int, **kwargs: Any) -> ThreadMessage:
        """Update a message in a thread."""
        res = self._client.request("PUT", f"collaboration/messages/{id}", json=kwargs)
        return ThreadMessage.model_validate(res)

    def delete_thread_message(self, id: int) -> None:
        """Delete a message from a thread."""
        self._client.request("DELETE", f"collaboration/messages/{id}")

    def get_quoted_text(self, id: int) -> Any:
        """Get quoted text for a message."""
        return self._client.request("GET", f"collaboration/messages/{id}/generate-quote")


class AsyncMinorResourcesAPI:
    """Asynchronous implementation of Minor APIs (Jobs, Settings, Threads)."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Jobs
    async def view_job(self, id: str) -> Job:
        """View a job by ID."""
        res = await self._client.request("GET", f"jobs/{id}")
        return Job.model_validate(res)

    # Settings
    async def view_helpdesk_settings(self) -> Setting:
        """View helpdesk settings."""
        res = await self._client.request("GET", "settings/helpdesk")
        return Setting.model_validate(res)

    # Threads
    async def create_thread(self, **kwargs: Any) -> Thread:
        """Create a thread."""
        res = await self._client.request("POST", "collaboration/threads", json=kwargs)
        return Thread.model_validate(res)

    async def get_thread(self, id: int) -> Thread:
        """Get a thread."""
        res = await self._client.request("GET", f"collaboration/threads/{id}")
        return Thread.model_validate(res)

    async def update_thread(self, id: int, **kwargs: Any) -> Thread:
        """Update a thread."""
        res = await self._client.request("PUT", f"collaboration/threads/{id}", json=kwargs)
        return Thread.model_validate(res)

    async def delete_thread(self, id: int) -> None:
        """Delete a thread."""
        await self._client.request("DELETE", f"collaboration/threads/{id}")

    # Thread messages
    async def create_thread_message(self, **kwargs: Any) -> ThreadMessage:
        """Create a message for a thread."""
        res = await self._client.request("POST", "collaboration/messages", json=kwargs)
        return ThreadMessage.model_validate(res)

    async def get_thread_message(self, id: int) -> ThreadMessage:
        """Get a message from a thread."""
        res = await self._client.request("GET", f"collaboration/messages/{id}")
        return ThreadMessage.model_validate(res)

    async def update_thread_message(self, id: int, **kwargs: Any) -> ThreadMessage:
        """Update a message in a thread."""
        res = await self._client.request("PUT", f"collaboration/messages/{id}", json=kwargs)
        return ThreadMessage.model_validate(res)

    async def delete_thread_message(self, id: int) -> None:
        """Delete a message from a thread."""
        await self._client.request("DELETE", f"collaboration/messages/{id}")

    async def get_quoted_text(self, id: int) -> Any:
        """Get quoted text for a message."""
        return await self._client.request("GET", f"collaboration/messages/{id}/generate-quote")
