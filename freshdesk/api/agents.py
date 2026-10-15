from __future__ import annotations
from typing import TYPE_CHECKING, Any, AsyncIterator, Iterator, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.agents import Agent

class AgentsAPI:
    """Synchronous implementation of the Agents API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create(self, **kwargs: Any) -> Agent:
        """Create a new agent."""
        res = self._client.request("POST", "agents", json=kwargs)
        return Agent.model_validate(res)

    def view(self, id: int) -> Agent:
        """View an agent by ID."""
        res = self._client.request("GET", f"agents/{id}")
        return Agent.model_validate(res)
        
    def me(self) -> Agent:
        """Currently authenticated agent."""
        res = self._client.request("GET", "agents/me")
        return Agent.model_validate(res)

    def list(self, **kwargs: Any) -> List[Agent]:
        """List all agents."""
        res = self._client.request("GET", "agents", params=kwargs)
        return [Agent.model_validate(c) for c in res]

    def iter_all(self, **kwargs: Any) -> Iterator[Agent]:
        """Iterate over all agents, fetching pages lazily (see ``list`` for filters)."""
        return self._client.paginate("agents", Agent, kwargs)
        
    def search(self, term: str) -> List[Agent]:
        """Search agents by term autocomplete."""
        res = self._client.request("GET", "agents/autocomplete", params={"term": term})
        return [Agent.model_validate(c) for c in res]

    def update(self, id: int, **kwargs: Any) -> Agent:
        """Update an agent."""
        res = self._client.request("PUT", f"agents/{id}", json=kwargs)
        return Agent.model_validate(res)

    def delete(self, id: int) -> None:
        """Delete an agent."""
        self._client.request("DELETE", f"agents/{id}")


class AsyncAgentsAPI:
    """Asynchronous implementation of the Agents API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def create(self, **kwargs: Any) -> Agent:
        """Create a new agent."""
        res = await self._client.request("POST", "agents", json=kwargs)
        return Agent.model_validate(res)

    async def view(self, id: int) -> Agent:
        """View an agent by ID."""
        res = await self._client.request("GET", f"agents/{id}")
        return Agent.model_validate(res)
        
    async def me(self) -> Agent:
        """Currently authenticated agent."""
        res = await self._client.request("GET", "agents/me")
        return Agent.model_validate(res)

    async def list(self, **kwargs: Any) -> List[Agent]:
        """List all agents."""
        res = await self._client.request("GET", "agents", params=kwargs)
        return [Agent.model_validate(c) for c in res]

    def iter_all(self, **kwargs: Any) -> AsyncIterator[Agent]:
        """Iterate over all agents, fetching pages lazily (see ``list`` for filters)."""
        return self._client.paginate("agents", Agent, kwargs)
        
    async def search(self, term: str) -> List[Agent]:
        """Search agents by term autocomplete."""
        res = await self._client.request("GET", "agents/autocomplete", params={"term": term})
        return [Agent.model_validate(c) for c in res]

    async def update(self, id: int, **kwargs: Any) -> Agent:
        """Update an agent."""
        res = await self._client.request("PUT", f"agents/{id}", json=kwargs)
        return Agent.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete an agent."""
        await self._client.request("DELETE", f"agents/{id}")
