from __future__ import annotations
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.skills import Skill

class SkillsAPI:
    """Synchronous implementation of the Skills API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create(self, **kwargs: Any) -> Skill:
        """Create a new skill."""
        res = self._client.request("POST", "admin/skills", json=kwargs)
        return Skill.model_validate(res)

    def view(self, id: int) -> Skill:
        """View a skill by ID."""
        res = self._client.request("GET", f"admin/skills/{id}")
        return Skill.model_validate(res)

    def list(self, **kwargs: Any) -> List[Skill]:
        """List all skills."""
        res = self._client.request("GET", "admin/skills", params=kwargs)
        return [Skill.model_validate(s) for s in res]

    def update(self, id: int, **kwargs: Any) -> Skill:
        """Update a skill."""
        res = self._client.request("PUT", f"admin/skills/{id}", json=kwargs)
        return Skill.model_validate(res)

    def delete(self, id: int) -> None:
        """Delete a skill."""
        self._client.request("DELETE", f"admin/skills/{id}")


class AsyncSkillsAPI:
    """Asynchronous implementation of the Skills API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def create(self, **kwargs: Any) -> Skill:
        """Create a new skill."""
        res = await self._client.request("POST", "admin/skills", json=kwargs)
        return Skill.model_validate(res)

    async def view(self, id: int) -> Skill:
        """View a skill by ID."""
        res = await self._client.request("GET", f"admin/skills/{id}")
        return Skill.model_validate(res)

    async def list(self, **kwargs: Any) -> List[Skill]:
        """List all skills."""
        res = await self._client.request("GET", "admin/skills", params=kwargs)
        return [Skill.model_validate(s) for s in res]

    async def update(self, id: int, **kwargs: Any) -> Skill:
        """Update a skill."""
        res = await self._client.request("PUT", f"admin/skills/{id}", json=kwargs)
        return Skill.model_validate(res)

    async def delete(self, id: int) -> None:
        """Delete a skill."""
        await self._client.request("DELETE", f"admin/skills/{id}")
