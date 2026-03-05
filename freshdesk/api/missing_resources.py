from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.missing_resources import (
    AgentAvailability,
    AdminGroup,
    OmnichannelActivity,
    ServiceTask,
    ServiceGroup,
    FieldTechnician,
)

class MissingResourcesAPI:
    """Synchronous implementation of Availability, Admin-Groups, Omnichannel, and Field Service Management."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Availability
    def list_agent_availability(self, **kwargs: Any) -> List[AgentAvailability]:
        """List all agents' availability."""
        kwargs["only"] = "availability"
        res = self._client.request("GET", "agents", params=kwargs)
        # the response includes normal agent attributes too, but pydantic ignores extras
        return [AgentAvailability.model_validate(a) for a in res]

    def view_agent_availability(self, id: int) -> AgentAvailability:
        """View a specific agent's availability."""
        res = self._client.request("GET", f"agents/{id}/availability")
        return AgentAvailability.model_validate(res)

    def update_agent_availability(self, id: int, **kwargs: Any) -> AgentAvailability:
        """Update an agent's availability settings."""
        res = self._client.request("PUT", f"agents/{id}/availability", json=kwargs)
        return AgentAvailability.model_validate(res)

    # Admin Groups
    def create_admin_group(self, **kwargs: Any) -> AdminGroup:
        """Create an Admin Group."""
        res = self._client.request("POST", "admin/groups", json=kwargs)
        return AdminGroup.model_validate(res)

    def view_admin_group(self, id: int) -> AdminGroup:
        """View an Admin Group."""
        res = self._client.request("GET", f"admin/groups/{id}")
        return AdminGroup.model_validate(res)

    def update_admin_group(self, id: int, **kwargs: Any) -> AdminGroup:
        """Update an Admin Group."""
        res = self._client.request("PUT", f"admin/groups/{id}", json=kwargs)
        return AdminGroup.model_validate(res)

    def delete_admin_group(self, id: int) -> None:
        """Delete an Admin Group."""
        self._client.request("DELETE", f"admin/groups/{id}")

    # Omnichannel Activities
    def publish_activity(self, **kwargs: Any) -> OmnichannelActivity:
        """Publish an Omnichannel Activity."""
        res = self._client.request("POST", "contact-activities", json=kwargs)
        return OmnichannelActivity.model_validate(res)

    # Field Service Management
    def create_service_task(self, **kwargs: Any) -> ServiceTask:
        """Create a FSM service task."""
        res = self._client.request("POST", "fsm/tasks", json=kwargs)
        return ServiceTask.model_validate(res)

    def list_service_tasks(self, **kwargs: Any) -> List[ServiceTask]:
        """List FSM service tasks."""
        res = self._client.request("GET", "fsm/tasks", params=kwargs)
        return [ServiceTask.model_validate(s) for s in res]

    def list_service_groups(self, **kwargs: Any) -> List[ServiceGroup]:
        """List FSM service groups."""
        res = self._client.request("GET", "fsm/groups", params=kwargs)
        return [ServiceGroup.model_validate(s) for s in res]

    def list_field_technicians(self, **kwargs: Any) -> List[FieldTechnician]:
        """List Field Technicians."""
        res = self._client.request("GET", "fsm/technicians", params=kwargs)
        return [FieldTechnician.model_validate(t) for t in res]


class AsyncMissingResourcesAPI:
    """Asynchronous implementation of Availability, Admin-Groups, Omnichannel, and Field Service Management."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Availability
    async def list_agent_availability(self, **kwargs: Any) -> List[AgentAvailability]:
        """List all agents' availability."""
        kwargs["only"] = "availability"
        res = await self._client.request("GET", "agents", params=kwargs)
        return [AgentAvailability.model_validate(a) for a in res]

    async def view_agent_availability(self, id: int) -> AgentAvailability:
        """View a specific agent's availability."""
        res = await self._client.request("GET", f"agents/{id}/availability")
        return AgentAvailability.model_validate(res)

    async def update_agent_availability(self, id: int, **kwargs: Any) -> AgentAvailability:
        """Update an agent's availability settings."""
        res = await self._client.request("PUT", f"agents/{id}/availability", json=kwargs)
        return AgentAvailability.model_validate(res)

    # Admin Groups
    async def create_admin_group(self, **kwargs: Any) -> AdminGroup:
        """Create an Admin Group."""
        res = await self._client.request("POST", "admin/groups", json=kwargs)
        return AdminGroup.model_validate(res)

    async def view_admin_group(self, id: int) -> AdminGroup:
        """View an Admin Group."""
        res = await self._client.request("GET", f"admin/groups/{id}")
        return AdminGroup.model_validate(res)

    async def update_admin_group(self, id: int, **kwargs: Any) -> AdminGroup:
        """Update an Admin Group."""
        res = await self._client.request("PUT", f"admin/groups/{id}", json=kwargs)
        return AdminGroup.model_validate(res)

    async def delete_admin_group(self, id: int) -> None:
        """Delete an Admin Group."""
        await self._client.request("DELETE", f"admin/groups/{id}")

    # Omnichannel Activities
    async def publish_activity(self, **kwargs: Any) -> OmnichannelActivity:
        """Publish an Omnichannel Activity."""
        res = await self._client.request("POST", "contact-activities", json=kwargs)
        return OmnichannelActivity.model_validate(res)

    # Field Service Management
    async def create_service_task(self, **kwargs: Any) -> ServiceTask:
        """Create a FSM service task."""
        res = await self._client.request("POST", "fsm/tasks", json=kwargs)
        return ServiceTask.model_validate(res)

    async def list_service_tasks(self, **kwargs: Any) -> List[ServiceTask]:
        """List FSM service tasks."""
        res = await self._client.request("GET", "fsm/tasks", params=kwargs)
        return [ServiceTask.model_validate(s) for s in res]

    async def list_service_groups(self, **kwargs: Any) -> List[ServiceGroup]:
        """List FSM service groups."""
        res = await self._client.request("GET", "fsm/groups", params=kwargs)
        return [ServiceGroup.model_validate(s) for s in res]

    async def list_field_technicians(self, **kwargs: Any) -> List[FieldTechnician]:
        """List Field Technicians."""
        res = await self._client.request("GET", "fsm/technicians", params=kwargs)
        return [FieldTechnician.model_validate(t) for t in res]
