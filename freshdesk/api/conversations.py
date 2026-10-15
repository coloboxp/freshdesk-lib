from __future__ import annotations
from typing import TYPE_CHECKING, Any, AsyncIterator, Iterator, List, Optional, Sequence

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.conversations import Conversation
from ._common import AttachmentInput, body_kwargs

class ConversationsAPI:
    """Synchronous implementation of the Conversations API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def list(
        self, ticket_id: int, page: Optional[int] = None
    ) -> List[Conversation]:
        """List one page (30 entries) of a ticket's conversations, oldest first.

        ``tickets.view(id, include="conversations")`` returns only 10; use
        this or :meth:`iter_all` for the full thread.
        """
        params = {"page": page} if page else None
        res = self._client.request(
            "GET", f"tickets/{ticket_id}/conversations", params=params
        )
        return [Conversation.model_validate(c) for c in res]

    def iter_all(self, ticket_id: int, **kwargs: Any) -> Iterator[Conversation]:
        """Iterate over all conversations of a ticket, fetching pages lazily."""
        return self._client.paginate(
            f"tickets/{ticket_id}/conversations", Conversation, kwargs
        )

    def create_reply(
        self,
        ticket_id: int,
        attachments: Optional[Sequence[AttachmentInput]] = None,
        **kwargs: Any,
    ) -> Conversation:
        """Create a reply to a ticket.  *attachments* switches to a multipart upload."""
        res = self._client.request(
            "POST", f"tickets/{ticket_id}/reply", **body_kwargs(kwargs, attachments)
        )
        return Conversation.model_validate(res)

    def create_note(
        self,
        ticket_id: int,
        attachments: Optional[Sequence[AttachmentInput]] = None,
        **kwargs: Any,
    ) -> Conversation:
        """Create a note on a ticket.  *attachments* switches to a multipart upload."""
        res = self._client.request(
            "POST", f"tickets/{ticket_id}/notes", **body_kwargs(kwargs, attachments)
        )
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

    async def list(
        self, ticket_id: int, page: Optional[int] = None
    ) -> List[Conversation]:
        """List one page (30 entries) of a ticket's conversations, oldest first.

        ``tickets.view(id, include="conversations")`` returns only 10; use
        this or :meth:`iter_all` for the full thread.
        """
        params = {"page": page} if page else None
        res = await self._client.request(
            "GET", f"tickets/{ticket_id}/conversations", params=params
        )
        return [Conversation.model_validate(c) for c in res]

    def iter_all(self, ticket_id: int, **kwargs: Any) -> AsyncIterator[Conversation]:
        """Iterate over all conversations of a ticket, fetching pages lazily."""
        return self._client.paginate(
            f"tickets/{ticket_id}/conversations", Conversation, kwargs
        )

    async def create_reply(
        self,
        ticket_id: int,
        attachments: Optional[Sequence[AttachmentInput]] = None,
        **kwargs: Any,
    ) -> Conversation:
        """Create a reply to a ticket.  *attachments* switches to a multipart upload."""
        res = await self._client.request(
            "POST", f"tickets/{ticket_id}/reply", **body_kwargs(kwargs, attachments)
        )
        return Conversation.model_validate(res)

    async def create_note(
        self,
        ticket_id: int,
        attachments: Optional[Sequence[AttachmentInput]] = None,
        **kwargs: Any,
    ) -> Conversation:
        """Create a note on a ticket.  *attachments* switches to a multipart upload."""
        res = await self._client.request(
            "POST", f"tickets/{ticket_id}/notes", **body_kwargs(kwargs, attachments)
        )
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
