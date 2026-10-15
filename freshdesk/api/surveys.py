from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.surveys import Survey, SatisfactionRating

class SurveysAPI:
    """Synchronous implementation of the Surveys API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def list_surveys(self, **kwargs: Any) -> List[Survey]:
        """List all surveys."""
        res = self._client.request("GET", "surveys", params=kwargs)
        return [Survey.model_validate(s) for s in res]

    def list_satisfaction_ratings(self, **kwargs: Any) -> List[SatisfactionRating]:
        """View all satisfaction ratings."""
        res = self._client.request("GET", "surveys/satisfaction_ratings", params=kwargs)
        return [SatisfactionRating.model_validate(r) for r in res]

    def list_ticket_satisfaction_ratings(self, ticket_id: int) -> List[SatisfactionRating]:
        """View the satisfaction ratings of one ticket.

        Unlike :meth:`list_satisfaction_ratings`, which needs an admin, any agent who can see the ticket may call it.
        """
        res = self._client.request("GET", f"tickets/{ticket_id}/satisfaction_ratings")
        return [SatisfactionRating.model_validate(r) for r in res]


class AsyncSurveysAPI:
    """Asynchronous implementation of the Surveys API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def list_surveys(self, **kwargs: Any) -> List[Survey]:
        """List all surveys."""
        res = await self._client.request("GET", "surveys", params=kwargs)
        return [Survey.model_validate(s) for s in res]

    async def list_satisfaction_ratings(self, **kwargs: Any) -> List[SatisfactionRating]:
        """View all satisfaction ratings."""
        res = await self._client.request("GET", "surveys/satisfaction_ratings", params=kwargs)
        return [SatisfactionRating.model_validate(r) for r in res]

    async def list_ticket_satisfaction_ratings(self, ticket_id: int) -> List[SatisfactionRating]:
        """View the satisfaction ratings of one ticket (any agent who can see the ticket)."""
        res = await self._client.request("GET", f"tickets/{ticket_id}/satisfaction_ratings")
        return [SatisfactionRating.model_validate(r) for r in res]
