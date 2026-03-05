from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.fields import TicketField, ContactField, CompanyField

class FieldsAPI:
    """Synchronous implementation of API resource Fields."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Ticket Fields
    def list_ticket_fields(self, **kwargs: Any) -> List[TicketField]:
        """List all ticket fields."""
        res = self._client.request("GET", "ticket_fields", params=kwargs)
        return [TicketField.model_validate(f) for f in res]
        
    def list_contact_fields(self, **kwargs: Any) -> List[ContactField]:
        """List all contact fields."""
        res = self._client.request("GET", "contact_fields", params=kwargs)
        return [ContactField.model_validate(f) for f in res]
        
    def list_company_fields(self, **kwargs: Any) -> List[CompanyField]:
        """List all company fields."""
        res = self._client.request("GET", "company_fields", params=kwargs)
        return [CompanyField.model_validate(f) for f in res]


class AsyncFieldsAPI:
    """Asynchronous implementation of API resource Fields."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Ticket Fields
    async def list_ticket_fields(self, **kwargs: Any) -> List[TicketField]:
        """List all ticket fields."""
        res = await self._client.request("GET", "ticket_fields", params=kwargs)
        return [TicketField.model_validate(f) for f in res]
        
    async def list_contact_fields(self, **kwargs: Any) -> List[ContactField]:
        """List all contact fields."""
        res = await self._client.request("GET", "contact_fields", params=kwargs)
        return [ContactField.model_validate(f) for f in res]
        
    async def list_company_fields(self, **kwargs: Any) -> List[CompanyField]:
        """List all company fields."""
        res = await self._client.request("GET", "company_fields", params=kwargs)
        return [CompanyField.model_validate(f) for f in res]
