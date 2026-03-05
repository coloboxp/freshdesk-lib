from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.automations import ScenarioAutomation, SLAPolicy, AutomationRule

class AutomationsAPI:
    """Synchronous implementation of Automations, SLA Policies, and Scenario Automations."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Scenario Automations
    def list_scenario_automations(self) -> List[ScenarioAutomation]:
        """List all scenario automations."""
        res = self._client.request("GET", "scenario_automations")
        return [ScenarioAutomation.model_validate(s) for s in res]

    # SLA Policies
    def create_sla_policy(self, **kwargs: Any) -> SLAPolicy:
        """Create an SLA policy."""
        res = self._client.request("POST", "sla_policies", json=kwargs)
        return SLAPolicy.model_validate(res)

    def list_sla_policies(self, **kwargs: Any) -> List[SLAPolicy]:
        """List all SLA policies."""
        res = self._client.request("GET", "sla_policies", params=kwargs)
        return [SLAPolicy.model_validate(s) for s in res]

    def update_sla_policy(self, id: int, **kwargs: Any) -> SLAPolicy:
        """Update an SLA policy."""
        res = self._client.request("PUT", f"sla_policies/{id}", json=kwargs)
        return SLAPolicy.model_validate(res)

    # Automations (Rules)
    def list_automation_rules(self, automation_type_id: int) -> List[AutomationRule]:
        """List all automation rules."""
        res = self._client.request("GET", f"automations/{automation_type_id}/rules")
        return [AutomationRule.model_validate(a) for a in res]

    def view_automation_rule(self, automation_type_id: int, id: int) -> AutomationRule:
        """View an automation rule."""
        res = self._client.request("GET", f"automations/{automation_type_id}/rules/{id}")
        return AutomationRule.model_validate(res)

    def delete_automation_rule(self, automation_type_id: int, id: int) -> None:
        """Delete an automation rule."""
        self._client.request("DELETE", f"automations/{automation_type_id}/rules/{id}")

    def create_automation_rule(self, automation_type_id: int, **kwargs: Any) -> AutomationRule:
        """Create an automation rule."""
        res = self._client.request("POST", f"automations/{automation_type_id}/rules", json=kwargs)
        return AutomationRule.model_validate(res)

    def update_automation_rule(self, automation_type_id: int, id: int, **kwargs: Any) -> AutomationRule:
        """Update an automation rule."""
        res = self._client.request("PUT", f"automations/{automation_type_id}/rules/{id}", json=kwargs)
        return AutomationRule.model_validate(res)


class AsyncAutomationsAPI:
    """Asynchronous implementation of Automations, SLA Policies, and Scenario Automations."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Scenario Automations
    async def list_scenario_automations(self) -> List[ScenarioAutomation]:
        """List all scenario automations."""
        res = await self._client.request("GET", "scenario_automations")
        return [ScenarioAutomation.model_validate(s) for s in res]

    # SLA Policies
    async def create_sla_policy(self, **kwargs: Any) -> SLAPolicy:
        """Create an SLA policy."""
        res = await self._client.request("POST", "sla_policies", json=kwargs)
        return SLAPolicy.model_validate(res)

    async def list_sla_policies(self, **kwargs: Any) -> List[SLAPolicy]:
        """List all SLA policies."""
        res = await self._client.request("GET", "sla_policies", params=kwargs)
        return [SLAPolicy.model_validate(s) for s in res]

    async def update_sla_policy(self, id: int, **kwargs: Any) -> SLAPolicy:
        """Update an SLA policy."""
        res = await self._client.request("PUT", f"sla_policies/{id}", json=kwargs)
        return SLAPolicy.model_validate(res)

    # Automations (Rules)
    async def list_automation_rules(self, automation_type_id: int) -> List[AutomationRule]:
        """List all automation rules."""
        res = await self._client.request("GET", f"automations/{automation_type_id}/rules")
        return [AutomationRule.model_validate(a) for a in res]

    async def view_automation_rule(self, automation_type_id: int, id: int) -> AutomationRule:
        """View an automation rule."""
        res = await self._client.request("GET", f"automations/{automation_type_id}/rules/{id}")
        return AutomationRule.model_validate(res)

    async def delete_automation_rule(self, automation_type_id: int, id: int) -> None:
        """Delete an automation rule."""
        await self._client.request("DELETE", f"automations/{automation_type_id}/rules/{id}")

    async def create_automation_rule(self, automation_type_id: int, **kwargs: Any) -> AutomationRule:
        """Create an automation rule."""
        res = await self._client.request("POST", f"automations/{automation_type_id}/rules", json=kwargs)
        return AutomationRule.model_validate(res)

    async def update_automation_rule(self, automation_type_id: int, id: int, **kwargs: Any) -> AutomationRule:
        """Update an automation rule."""
        res = await self._client.request("PUT", f"automations/{automation_type_id}/rules/{id}", json=kwargs)
        return AutomationRule.model_validate(res)
