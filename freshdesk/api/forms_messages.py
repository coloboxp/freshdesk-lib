from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.forms_messages import TicketForm, OutboundMessage

class FormsMessagesAPI:
    """Synchronous implementation of Ticket Forms and Outbound Messages."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Ticket Forms
    def list_ticket_forms(self) -> List[TicketForm]:
        """List all ticket forms."""
        res = self._client.request("GET", "ticket_forms")
        return [TicketForm.model_validate(f) for f in res]

    def view_ticket_form(self, id: int) -> TicketForm:
        """View a ticket form."""
        res = self._client.request("GET", f"ticket_forms/{id}")
        return TicketForm.model_validate(res)

    # Outbound Messages
    def send_outbound_message(self, **kwargs: Any) -> OutboundMessage:
        """Send a proactive outbound message."""
        res = self._client.request("POST", "channels/outbound-messages", json=kwargs)
        return OutboundMessage.model_validate(res)

    def retrieve_outbound_message(self, id: int) -> OutboundMessage:
        """Retrieve an outbound message."""
        res = self._client.request("GET", f"channels/outbound-messages/{id}")
        return OutboundMessage.model_validate(res)


class AsyncFormsMessagesAPI:
    """Asynchronous implementation of Ticket Forms and Outbound Messages."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Ticket Forms
    async def list_ticket_forms(self) -> List[TicketForm]:
        """List all ticket forms."""
        res = await self._client.request("GET", "ticket_forms")
        return [TicketForm.model_validate(f) for f in res]

    async def view_ticket_form(self, id: int) -> TicketForm:
        """View a ticket form."""
        res = await self._client.request("GET", f"ticket_forms/{id}")
        return TicketForm.model_validate(res)

    # Outbound Messages
    async def send_outbound_message(self, **kwargs: Any) -> OutboundMessage:
        """Send a proactive outbound message."""
        res = await self._client.request("POST", "channels/outbound-messages", json=kwargs)
        return OutboundMessage.model_validate(res)

    async def retrieve_outbound_message(self, id: int) -> OutboundMessage:
        """Retrieve an outbound message."""
        res = await self._client.request("GET", f"channels/outbound-messages/{id}")
        return OutboundMessage.model_validate(res)
