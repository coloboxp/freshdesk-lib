from __future__ import annotations
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.companies import Company

class CompaniesAPI:
    """Synchronous implementation of the Companies API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create(self, **kwargs: Any) -> Company:
        """Create a new company."""
        res = self._client.request("POST", "companies", json=kwargs)
        return Company.model_validate(res)

    def view(self, id: int) -> Company:
        """View a company by ID."""
        res = self._client.request("GET", f"companies/{id}")
        return Company.model_validate(res)

    def list(self, **kwargs: Any) -> List[Company]:
        """List all companies."""
        res = self._client.request("GET", "companies", params=kwargs)
        return [Company.model_validate(c) for c in res]
        
    def filter(self, query: str) -> List[Company]:
        """Filter companies using a query string."""
        res = self._client.request("GET", "search/companies", params={"query": query})
        return [Company.model_validate(c) for c in res.get("results", [])]
        
    def search(self, name: str) -> List[Company]:
        """Search companies by name autocomplete."""
        res = self._client.request("GET", "companies/autocomplete", params={"name": name})
        return [Company.model_validate(c) for c in res]

    def update(self, id: int, **kwargs: Any) -> Company:
        """Update a company."""
        res = self._client.request("PUT", f"companies/{id}", json=kwargs)
        return Company.model_validate(res)

    def delete(self, id: int) -> None:
        """Delete a company."""
        self._client.request("DELETE", f"companies/{id}")


class AsyncCompaniesAPI:
    """Asynchronous implementation of the Companies API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def create(self, **kwargs: Any) -> Company:
        """Create a new company."""
        res = await self._client.request("POST", "companies", json=kwargs)
        return Company.model_validate(res)

    async def view(self, id: int) -> Company:
        """View a company by ID."""
        res = await self._client.request("GET", f"companies/{id}")
        return Company.model_validate(res)

    async def list(self, **kwargs: Any) -> List[Company]:
        """List all companies."""
        res = await self._client.request("GET", "companies", params=kwargs)
        return [Company.model_validate(c) for c in res]
        
    async def filter(self, query: str) -> List[Company]:
        """Filter companies using a query string."""
        res = await self._client.request("GET", "search/companies", params={"query": query})
        return [Company.model_validate(c) for c in res.get("results", [])]
        
    async def search(self, name: str) -> List[Company]:
        """Search companies by name autocomplete."""
        res = await self._client.request("GET", "companies/autocomplete", params={"name": name})
        return [Company.model_validate(c) for c in res]

    async def update(self, id: int, **kwargs: Any) -> Company:
        """Update a company."""
        res = await self._client.request("PUT", f"companies/{id}", json=kwargs)
        return Company.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete a company."""
        await self._client.request("DELETE", f"companies/{id}")
