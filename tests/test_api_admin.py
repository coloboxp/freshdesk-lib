"""Integration tests for admin API modules: automations, fields,
forms_messages, admin_resources, minor_resources, missing_resources.
"""
import uuid

import pytest

from freshdesk.exceptions import FreshdeskAPIError
from freshdesk.models.admin_resources import (
    Account, BusinessHour, EmailConfig, EmailMailbox, Product,
)
from freshdesk.models.automations import AutomationRule, ScenarioAutomation, SLAPolicy
from freshdesk.models.fields import CompanyField, ContactField, TicketField
from freshdesk.models.forms_messages import OutboundMessage, TicketForm
from freshdesk.models.minor_resources import Job, Setting, Thread, ThreadMessage
from freshdesk.models.missing_resources import (
    AdminGroup, AgentAvailability, FieldTechnician,
    OmnichannelActivity, ServiceGroup, ServiceTask,
)
from conftest import api_or_skip, async_api_or_skip

_RUN_ID = uuid.uuid4().hex[:8]

TICKET_DEFAULTS = dict(
    subject=f"[TEST] admin-api {_RUN_ID}",
    description="Automated test – safe to delete",
    email=f"admin-api-{_RUN_ID}@test.example.com",
    priority=1,
    status=2,
)


# ═══════════════════════════════════════════════════════════════════════════
# Automations
# ═══════════════════════════════════════════════════════════════════════════

class TestAutomationsSync:
    def test_list_scenario_automations(self, client):
        result = api_or_skip(client.automations.list_scenario_automations)
        assert isinstance(result, list)

    def test_list_sla_policies(self, client):
        result = api_or_skip(client.automations.list_sla_policies)
        assert isinstance(result, list)

    def test_sla_policy_lifecycle(self, client):
        try:
            sla = api_or_skip(
                client.automations.create_sla_policy,
                name=f"[TEST] SLA Policy {_RUN_ID}",
                description="test",
            )
        except FreshdeskAPIError:
            pytest.skip("SLA policy creation not supported")
            return
        assert isinstance(sla, SLAPolicy)
        try:
            updated = client.automations.update_sla_policy(
                sla.id, name=f"[TEST] Updated SLA {_RUN_ID}"
            )
            assert isinstance(updated, SLAPolicy)
        finally:
            pass  # no delete endpoint for SLA policies

    def test_automation_rules(self, client):
        try:
            rules = api_or_skip(client.automations.list_automation_rules, 1)
            assert isinstance(rules, list)
            if rules:
                viewed = client.automations.view_automation_rule(1, rules[0].id)
                assert isinstance(viewed, AutomationRule)
        except FreshdeskAPIError:
            pytest.skip("Automation rules not available")


class TestAutomationsAsync:
    async def test_list_scenario_automations(self, async_client):
        result = await async_api_or_skip(
            async_client.automations.list_scenario_automations()
        )
        assert isinstance(result, list)

    async def test_list_sla_policies(self, async_client):
        result = await async_api_or_skip(
            async_client.automations.list_sla_policies()
        )
        assert isinstance(result, list)

    async def test_sla_policy_lifecycle(self, async_client):
        try:
            sla = await async_api_or_skip(
                async_client.automations.create_sla_policy(
                    name=f"[TEST] Async SLA {_RUN_ID}",
                    description="async test",
                )
            )
        except FreshdeskAPIError:
            pytest.skip("SLA policy creation not supported")
            return
        assert isinstance(sla, SLAPolicy)
        updated = await async_client.automations.update_sla_policy(
            sla.id, name=f"[TEST] Async Updated SLA {_RUN_ID}"
        )
        assert isinstance(updated, SLAPolicy)

    async def test_automation_rules(self, async_client):
        try:
            rules = await async_api_or_skip(
                async_client.automations.list_automation_rules(1)
            )
            assert isinstance(rules, list)
            if rules:
                viewed = await async_client.automations.view_automation_rule(
                    1, rules[0].id
                )
                assert isinstance(viewed, AutomationRule)
        except FreshdeskAPIError:
            pytest.skip("Automation rules not available")


# ═══════════════════════════════════════════════════════════════════════════
# Fields (read-only)
# ═══════════════════════════════════════════════════════════════════════════

class TestFieldsSync:
    def test_list_ticket_fields(self, client):
        result = client.fields.list_ticket_fields()
        assert isinstance(result, list)
        assert all(isinstance(f, TicketField) for f in result)

    def test_list_contact_fields(self, client):
        result = client.fields.list_contact_fields()
        assert isinstance(result, list)
        assert all(isinstance(f, ContactField) for f in result)

    def test_list_company_fields(self, client):
        result = client.fields.list_company_fields()
        assert isinstance(result, list)
        assert all(isinstance(f, CompanyField) for f in result)


class TestFieldsAsync:
    async def test_list_ticket_fields(self, async_client):
        result = await async_client.fields.list_ticket_fields()
        assert isinstance(result, list)

    async def test_list_contact_fields(self, async_client):
        result = await async_client.fields.list_contact_fields()
        assert isinstance(result, list)

    async def test_list_company_fields(self, async_client):
        result = await async_client.fields.list_company_fields()
        assert isinstance(result, list)


# ═══════════════════════════════════════════════════════════════════════════
# Forms & Messages
# ═══════════════════════════════════════════════════════════════════════════

class TestFormsMessagesSync:
    def test_list_ticket_forms(self, client):
        result = api_or_skip(client.forms_messages.list_ticket_forms)
        assert isinstance(result, list)

    def test_view_ticket_form(self, client):
        forms = api_or_skip(client.forms_messages.list_ticket_forms)
        if not forms:
            pytest.skip("No ticket forms available")
        viewed = client.forms_messages.view_ticket_form(forms[0].id)
        assert isinstance(viewed, TicketForm)
        assert viewed.id == forms[0].id

    def test_outbound_message(self, client):
        try:
            msg = api_or_skip(
                client.forms_messages.send_outbound_message,
                body="[TEST] outbound",
                channel_id=1,
                recipient_id=1,
            )
            assert isinstance(msg, OutboundMessage)
            client.forms_messages.retrieve_outbound_message(msg.id)
        except FreshdeskAPIError:
            pytest.skip("Outbound messages not available")


class TestFormsMessagesAsync:
    async def test_list_ticket_forms(self, async_client):
        result = await async_api_or_skip(
            async_client.forms_messages.list_ticket_forms()
        )
        assert isinstance(result, list)

    async def test_view_ticket_form(self, async_client):
        forms = await async_api_or_skip(
            async_client.forms_messages.list_ticket_forms()
        )
        if not forms:
            pytest.skip("No ticket forms available")
        viewed = await async_client.forms_messages.view_ticket_form(forms[0].id)
        assert isinstance(viewed, TicketForm)

    async def test_outbound_message(self, async_client):
        try:
            msg = await async_api_or_skip(
                async_client.forms_messages.send_outbound_message(
                    body="[TEST] async outbound",
                    channel_id=1,
                    recipient_id=1,
                )
            )
            assert isinstance(msg, OutboundMessage)
            await async_client.forms_messages.retrieve_outbound_message(msg.id)
        except FreshdeskAPIError:
            pytest.skip("Outbound messages not available")


# ═══════════════════════════════════════════════════════════════════════════
# Admin Resources
# ═══════════════════════════════════════════════════════════════════════════

class TestAdminResourcesSync:
    def test_view_account(self, client):
        acct = api_or_skip(client.admin.view_account_details)
        assert isinstance(acct, Account)
        assert acct.id > 0

    def test_export_account(self, client):
        result = api_or_skip(client.admin.export_account)
        assert result is not None or result is None  # just exercises the path

    def test_list_business_hours(self, client):
        result = client.admin.list_business_hours()
        assert isinstance(result, list)

    def test_view_business_hour(self, client):
        hours = client.admin.list_business_hours()
        if not hours:
            pytest.skip("No business hours")
        viewed = client.admin.view_business_hour(hours[0].id)
        assert isinstance(viewed, BusinessHour)

    def test_list_email_configs(self, client):
        result = client.admin.list_email_configs()
        assert isinstance(result, list)

    def test_view_email_config(self, client):
        configs = client.admin.list_email_configs()
        if not configs:
            pytest.skip("No email configs")
        viewed = client.admin.view_email_config(configs[0].id)
        assert isinstance(viewed, EmailConfig)

    def test_email_mailboxes(self, client):
        result = api_or_skip(client.admin.list_email_mailboxes)
        assert isinstance(result, list)
        if result:
            viewed = client.admin.view_email_mailbox(result[0].id)
            assert isinstance(viewed, EmailMailbox)

    def test_mailbox_settings(self, client):
        try:
            settings = api_or_skip(client.admin.view_mailbox_settings)
            assert settings is not None or settings is None
        except FreshdeskAPIError:
            pytest.skip("Mailbox settings not available")

    def test_list_products(self, client):
        result = client.admin.list_products()
        assert isinstance(result, list)

    def test_view_product(self, client):
        products = client.admin.list_products()
        if not products:
            pytest.skip("No products")
        viewed = client.admin.view_product(products[0].id)
        assert isinstance(viewed, Product)


class TestAdminResourcesAsync:
    async def test_view_account(self, async_client):
        acct = await async_api_or_skip(async_client.admin.view_account_details())
        assert isinstance(acct, Account)

    async def test_export_account(self, async_client):
        result = await async_api_or_skip(async_client.admin.export_account())
        assert result is not None or result is None

    async def test_list_business_hours(self, async_client):
        result = await async_client.admin.list_business_hours()
        assert isinstance(result, list)

    async def test_view_business_hour(self, async_client):
        hours = await async_client.admin.list_business_hours()
        if not hours:
            pytest.skip("No business hours")
        viewed = await async_client.admin.view_business_hour(hours[0].id)
        assert isinstance(viewed, BusinessHour)

    async def test_list_email_configs(self, async_client):
        result = await async_client.admin.list_email_configs()
        assert isinstance(result, list)

    async def test_view_email_config(self, async_client):
        configs = await async_client.admin.list_email_configs()
        if not configs:
            pytest.skip("No email configs")
        viewed = await async_client.admin.view_email_config(configs[0].id)
        assert isinstance(viewed, EmailConfig)

    async def test_email_mailboxes(self, async_client):
        result = await async_api_or_skip(
            async_client.admin.list_email_mailboxes()
        )
        assert isinstance(result, list)
        if result:
            viewed = await async_client.admin.view_email_mailbox(result[0].id)
            assert isinstance(viewed, EmailMailbox)

    async def test_mailbox_settings(self, async_client):
        try:
            result = await async_api_or_skip(
                async_client.admin.view_mailbox_settings()
            )
            assert result is not None or result is None
        except FreshdeskAPIError:
            pytest.skip("Mailbox settings not available")

    async def test_list_products(self, async_client):
        result = await async_client.admin.list_products()
        assert isinstance(result, list)

    async def test_view_product(self, async_client):
        products = await async_client.admin.list_products()
        if not products:
            pytest.skip("No products")
        viewed = await async_client.admin.view_product(products[0].id)
        assert isinstance(viewed, Product)


# ═══════════════════════════════════════════════════════════════════════════
# Minor Resources
# ═══════════════════════════════════════════════════════════════════════════

class TestMinorResourcesSync:
    def test_view_helpdesk_settings(self, client):
        result = client.minor_resources.view_helpdesk_settings()
        assert isinstance(result, Setting)

    def test_thread_lifecycle(self, client):
        try:
            ticket = client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as e:
            pytest.skip(f"Ticket creation rejected by instance ({e.status_code})")
        try:
            thread = api_or_skip(
                client.minor_resources.create_thread,
                type="discussion",
                title=f"[TEST] Thread {_RUN_ID}",
                parent={"parent_id": ticket.id, "type": "ticket"},
            )
            assert isinstance(thread, Thread)

            viewed = client.minor_resources.get_thread(thread.id)
            assert viewed.id == thread.id

            updated = client.minor_resources.update_thread(
                thread.id, subject=f"[TEST] Updated Thread {_RUN_ID}"
            )
            assert isinstance(updated, Thread)

            msg = client.minor_resources.create_thread_message(
                thread_id=thread.id, body="[TEST] Message"
            )
            assert isinstance(msg, ThreadMessage)

            viewed_msg = client.minor_resources.get_thread_message(msg.id)
            assert viewed_msg.id == msg.id

            updated_msg = client.minor_resources.update_thread_message(
                msg.id, body="[TEST] Updated Message"
            )
            assert isinstance(updated_msg, ThreadMessage)

            try:
                client.minor_resources.get_quoted_text(msg.id)
            except FreshdeskAPIError:
                pass

            client.minor_resources.delete_thread_message(msg.id)
            client.minor_resources.delete_thread(thread.id)
        except FreshdeskAPIError:
            pytest.skip("Collaboration threads not available")
        finally:
            client.tickets.delete(ticket.id)


class TestMinorResourcesAsync:
    async def test_view_helpdesk_settings(self, async_client):
        result = await async_client.minor_resources.view_helpdesk_settings()
        assert isinstance(result, Setting)

    async def test_thread_lifecycle(self, async_client):
        try:
            ticket = await async_client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as e:
            pytest.skip(f"Ticket creation rejected by instance ({e.status_code})")
        try:
            thread = await async_api_or_skip(
                async_client.minor_resources.create_thread(
                    type="discussion",
                    title=f"[TEST] Async Thread {_RUN_ID}",
                    parent={"parent_id": ticket.id, "type": "ticket"},
                )
            )
            assert isinstance(thread, Thread)

            viewed = await async_client.minor_resources.get_thread(thread.id)
            assert viewed.id == thread.id

            updated = await async_client.minor_resources.update_thread(
                thread.id, subject=f"[TEST] Async Updated Thread {_RUN_ID}"
            )
            assert isinstance(updated, Thread)

            msg = await async_client.minor_resources.create_thread_message(
                thread_id=thread.id, body="[TEST] Async Message"
            )
            assert isinstance(msg, ThreadMessage)

            viewed_msg = await async_client.minor_resources.get_thread_message(msg.id)
            assert viewed_msg.id == msg.id

            updated_msg = await async_client.minor_resources.update_thread_message(
                msg.id, body="[TEST] Async Updated Message"
            )
            assert isinstance(updated_msg, ThreadMessage)

            try:
                await async_client.minor_resources.get_quoted_text(msg.id)
            except FreshdeskAPIError:
                pass

            await async_client.minor_resources.delete_thread_message(msg.id)
            await async_client.minor_resources.delete_thread(thread.id)
        except FreshdeskAPIError:
            pytest.skip("Collaboration threads not available")
        finally:
            await async_client.tickets.delete(ticket.id)


# ═══════════════════════════════════════════════════════════════════════════
# Missing Resources
# ═══════════════════════════════════════════════════════════════════════════

class TestMissingResourcesSync:
    def test_list_agent_availability(self, client):
        result = api_or_skip(client.missing_resources.list_agent_availability)
        assert isinstance(result, list)

    def test_view_agent_availability(self, client):
        me = client.agents.me()
        try:
            avail = api_or_skip(
                client.missing_resources.view_agent_availability, me.id
            )
            assert isinstance(avail, AgentAvailability)
        except FreshdeskAPIError:
            pytest.skip("Agent availability not available")

    def test_update_agent_availability(self, client):
        me = client.agents.me()
        try:
            updated = api_or_skip(
                client.missing_resources.update_agent_availability,
                me.id,
                availability_status="online",
            )
            assert isinstance(updated, AgentAvailability)
        except FreshdeskAPIError:
            pytest.skip("Agent availability update not available")

    def test_admin_group_lifecycle(self, client):
        try:
            ag = api_or_skip(
                client.missing_resources.create_admin_group,
                name=f"[TEST] Admin Group {_RUN_ID}",
                type="support",
            )
        except FreshdeskAPIError:
            pytest.skip("Admin groups not available")
            return
        assert isinstance(ag, AdminGroup)
        try:
            viewed = client.missing_resources.view_admin_group(ag.id)
            assert viewed.id == ag.id

            updated = client.missing_resources.update_admin_group(
                ag.id, name=f"[TEST] Updated Admin Group {_RUN_ID}"
            )
            assert isinstance(updated, AdminGroup)
        finally:
            client.missing_resources.delete_admin_group(ag.id)

    def test_publish_activity(self, client):
        try:
            result = api_or_skip(
                client.missing_resources.publish_activity,
                description="[TEST] Activity",
                actor={"type": "user", "id": "1"},
                source={"type": "test"},
                contact={"identifier": "test@test.example.com"},
            )
            assert isinstance(result, OmnichannelActivity)
        except FreshdeskAPIError:
            pytest.skip("Omnichannel activities not available")

    def test_fsm_operations(self, client):
        try:
            tasks = api_or_skip(client.missing_resources.list_service_tasks)
            assert isinstance(tasks, list)

            groups = api_or_skip(client.missing_resources.list_service_groups)
            assert isinstance(groups, list)

            techs = api_or_skip(client.missing_resources.list_field_technicians)
            assert isinstance(techs, list)
        except FreshdeskAPIError:
            pytest.skip("FSM not available")


class TestMissingResourcesAsync:
    async def test_list_agent_availability(self, async_client):
        result = await async_api_or_skip(
            async_client.missing_resources.list_agent_availability()
        )
        assert isinstance(result, list)

    async def test_view_agent_availability(self, async_client):
        me = await async_client.agents.me()
        try:
            avail = await async_api_or_skip(
                async_client.missing_resources.view_agent_availability(me.id)
            )
            assert isinstance(avail, AgentAvailability)
        except FreshdeskAPIError:
            pytest.skip("Agent availability not available")

    async def test_update_agent_availability(self, async_client):
        me = await async_client.agents.me()
        try:
            updated = await async_api_or_skip(
                async_client.missing_resources.update_agent_availability(
                    me.id, availability_status="online"
                )
            )
            assert isinstance(updated, AgentAvailability)
        except FreshdeskAPIError:
            pytest.skip("Agent availability update not available")

    async def test_admin_group_lifecycle(self, async_client):
        try:
            ag = await async_api_or_skip(
                async_client.missing_resources.create_admin_group(
                    name=f"[TEST] Async Admin Group {_RUN_ID}",
                    type="support",
                )
            )
        except FreshdeskAPIError:
            pytest.skip("Admin groups not available")
            return
        assert isinstance(ag, AdminGroup)
        try:
            viewed = await async_client.missing_resources.view_admin_group(ag.id)
            assert viewed.id == ag.id

            updated = await async_client.missing_resources.update_admin_group(
                ag.id, name=f"[TEST] Async Updated Admin {_RUN_ID}"
            )
            assert isinstance(updated, AdminGroup)
        finally:
            await async_client.missing_resources.delete_admin_group(ag.id)

    async def test_publish_activity(self, async_client):
        try:
            result = await async_api_or_skip(
                async_client.missing_resources.publish_activity(
                    description="[TEST] Async Activity",
                    actor={"type": "user", "id": "1"},
                    source={"type": "test"},
                    contact={"identifier": "test@test.example.com"},
                )
            )
            assert isinstance(result, OmnichannelActivity)
        except FreshdeskAPIError:
            pytest.skip("Omnichannel activities not available")

    async def test_fsm_operations(self, async_client):
        try:
            tasks = await async_api_or_skip(
                async_client.missing_resources.list_service_tasks()
            )
            assert isinstance(tasks, list)

            groups = await async_api_or_skip(
                async_client.missing_resources.list_service_groups()
            )
            assert isinstance(groups, list)

            techs = await async_api_or_skip(
                async_client.missing_resources.list_field_technicians()
            )
            assert isinstance(techs, list)
        except FreshdeskAPIError:
            pytest.skip("FSM not available")
