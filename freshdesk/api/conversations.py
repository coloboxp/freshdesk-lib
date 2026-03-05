from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.conversations import Conversation

class ConversationsAPI:
    """Synchronous implementation of the Conversations API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create_reply(self, ticket_id: int, **kwargs: Any) -> Conversation:
        """Create a reply to a ticket."""
        res = self._client.request("POST", f"tickets/{ticket_id}/reply", json=kwargs)
        return Conversation.model_validate(res)

    def create_note(self, ticket_id: int, **kwargs: Any) -> Conversation:
        """Create a note on a ticket."""
        res = self._client.request("POST", f"tickets/{ticket_id}/notes", json=kwargs)
        return Conversation.model_validate(res)

    def update(self, id: int, **kwargs: Any) -> Conversation:
        """Update a conversation."""
        res = self._client.request("PUT", f"conversations/{id}", json=kwargs)
        return Conversation.model_validate(res)

    def delete(self, id: int) -> None:
        """Delete a conversation."""
        self._client.request("DELETE", f"conversations/{id}")

    def reply_to_forward(self, ticket_id: int, **kwargs: Any) -> Conversation:
        """Reply to a forward on a ticket."""
        res = self._client.request("POST", f"tickets/{ticket_id}/reply_to_forward", json=kwargs)
        return Conversation.model_validate(res)


class AsyncConversationsAPI:
    """Asynchronous implementation of the Conversations API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def create_reply(self, ticket_id: int, **kwargs: Any) -> Conversation:
        """Create a reply to a ticket."""
        res = await self._client.request("POST", f"tickets/{ticket_id}/reply", json=kwargs)
        return Conversation.model_validate(res)

    async def create_note(self, ticket_id: int, **kwargs: Any) -> Conversation:
        """Create a note on a ticket."""
        res = await self._client.request("POST", f"tickets/{ticket_id}/notes", json=kwargs)
        return Conversation.model_validate(res)

    async def update(self, id: int, **kwargs: Any) -> Conversation:
        """Update a conversation."""
        res = await self._client.request("PUT", f"conversations/{id}", json=kwargs)
        return Conversation.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete a conversation."""
        await self._client.request("DELETE", f"conversations/{id}")

    async def reply_to_forward(self, ticket_id: int, **kwargs: Any) -> Conversation:
        """Reply to a forward on a ticket."""
        res = await self._client.request("POST", f"tickets/{ticket_id}/reply_to_forward", json=kwargs)
        return Conversation.model_validate(res)
