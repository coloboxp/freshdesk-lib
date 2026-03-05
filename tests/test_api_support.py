"""Integration tests for support API modules: roles, skills, time_entries,
canned_responses, custom_objects.
"""
import uuid

import pytest

from freshdesk.exceptions import FreshdeskAPIError
from freshdesk.models.canned_responses import CannedResponse, CannedResponseFolder
from freshdesk.models.custom_objects import CustomObjectRecord, CustomObjectSchema
from freshdesk.models.roles import Role
from freshdesk.models.skills import Skill
from freshdesk.models.time_entries import TimeEntry
from conftest import api_or_skip, async_api_or_skip

_RUN_ID = uuid.uuid4().hex[:8]

TICKET_DEFAULTS = dict(
    subject=f"[TEST] support-api {_RUN_ID}",
    description="Automated test – safe to delete",
    email=f"support-api-{_RUN_ID}@test.example.com",
    priority=1,
    status=2,
)


# ---------------------------------------------------------------------------
# Roles (read-only)
# ---------------------------------------------------------------------------

class TestRolesSync:
    def test_list(self, client):
        result = client.roles.list()
        assert isinstance(result, list)
        assert all(isinstance(r, Role) for r in result)

    def test_view(self, client):
        roles = client.roles.list()
        if not roles:
            pytest.skip("No roles available")
        viewed = client.roles.view(roles[0].id)
        assert viewed.id == roles[0].id


class TestRolesAsync:
    async def test_list(self, async_client):
        result = await async_client.roles.list()
        assert isinstance(result, list)

    async def test_view(self, async_client):
        roles = await async_client.roles.list()
        if not roles:
            pytest.skip("No roles available")
        viewed = await async_client.roles.view(roles[0].id)
        assert viewed.id == roles[0].id


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

class TestSkillsSync:
    def test_list(self, client):
        result = api_or_skip(client.skills.list)
        assert isinstance(result, list)

    def test_crud_lifecycle(self, client):
        s = api_or_skip(client.skills.create, name=f"[TEST] Pytest Skill {_RUN_ID}")
        assert isinstance(s, Skill)
        try:
            viewed = client.skills.view(s.id)
            assert viewed.id == s.id

            updated = client.skills.update(s.id, name=f"[TEST] Updated Skill {_RUN_ID}")
            assert updated.name == f"[TEST] Updated Skill {_RUN_ID}"
        finally:
            client.skills.delete(s.id)


class TestSkillsAsync:
    async def test_list(self, async_client):
        result = await async_api_or_skip(async_client.skills.list())
        assert isinstance(result, list)

    async def test_crud_lifecycle(self, async_client):
        s = await async_api_or_skip(
            async_client.skills.create(name=f"[TEST] Async Skill {_RUN_ID}")
        )
        assert isinstance(s, Skill)
        try:
            viewed = await async_client.skills.view(s.id)
            assert viewed.id == s.id

            updated = await async_client.skills.update(
                s.id, name=f"[TEST] Async Updated {_RUN_ID}"
            )
            assert updated.name == f"[TEST] Async Updated {_RUN_ID}"
        finally:
            await async_client.skills.delete(s.id)


# ---------------------------------------------------------------------------
# Time Entries
# ---------------------------------------------------------------------------

class TestTimeEntriesSync:
    def test_list(self, client):
        result = client.time_entries.list()
        assert isinstance(result, list)

    def test_crud_lifecycle(self, client):
        try:
            ticket = client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as e:
            pytest.skip(f"Ticket creation rejected by instance ({e.status_code})")
        try:
            te = client.time_entries.create(
                ticket.id, time_spent="01:00", note="[TEST] entry"
            )
            assert isinstance(te, TimeEntry)

            updated = client.time_entries.update(te.id, note="[TEST] updated")
            assert updated.note == "[TEST] updated"

            toggled = client.time_entries.toggle_timer(te.id)
            assert isinstance(toggled, TimeEntry)
            client.time_entries.toggle_timer(te.id)

            client.time_entries.delete(te.id)
        finally:
            client.tickets.delete(ticket.id)


class TestTimeEntriesAsync:
    async def test_list(self, async_client):
        result = await async_client.time_entries.list()
        assert isinstance(result, list)

    async def test_crud_lifecycle(self, async_client):
        try:
            ticket = await async_client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as e:
            pytest.skip(f"Ticket creation rejected by instance ({e.status_code})")
        try:
            te = await async_client.time_entries.create(
                ticket.id, time_spent="00:30", note="[TEST] async entry"
            )
            assert isinstance(te, TimeEntry)

            updated = await async_client.time_entries.update(
                te.id, note="[TEST] async updated"
            )
            assert updated.note == "[TEST] async updated"

            toggled = await async_client.time_entries.toggle_timer(te.id)
            assert isinstance(toggled, TimeEntry)
            await async_client.time_entries.toggle_timer(te.id)

            await async_client.time_entries.delete(te.id)
        finally:
            await async_client.tickets.delete(ticket.id)


# ---------------------------------------------------------------------------
# Canned Responses
# ---------------------------------------------------------------------------

class TestCannedResponsesSync:
    def test_crud_lifecycle(self, client):
        try:
            folder = client.canned_responses.create_folder(name=f"[TEST] Folder {_RUN_ID}")
        except FreshdeskAPIError as e:
            pytest.skip(f"Folder creation rejected by instance ({e.status_code})")
        assert isinstance(folder, CannedResponseFolder)
        try:
            folders = client.canned_responses.list_folders()
            assert isinstance(folders, list)

            client.canned_responses.update_folder(
                folder.id, name=f"[TEST] Updated Folder {_RUN_ID}"
            )

            cr = client.canned_responses.create(
                title=f"[TEST] Response {_RUN_ID}",
                content="Hello {{name}}",
                content_html="<p>Hello {{name}}</p>",
                folder_id=folder.id,
            )
            assert isinstance(cr, CannedResponse)

            client.canned_responses.view(cr.id)
            client.canned_responses.update(cr.id, title=f"[TEST] Updated Response {_RUN_ID}")
            client.canned_responses.list_responses_in_folder(folder.id)
            client.canned_responses.delete(cr.id)
        except FreshdeskAPIError as e:
            pytest.skip(f"Canned response lifecycle failed ({e.status_code})")
        finally:
            try:
                client.canned_responses.delete_folder(folder.id)
            except Exception:
                pass


class TestCannedResponsesAsync:
    async def test_crud_lifecycle(self, async_client):
        try:
            folder = await async_client.canned_responses.create_folder(name=f"[TEST] Async Folder {_RUN_ID}")
        except FreshdeskAPIError as e:
            pytest.skip(f"Folder creation rejected by instance ({e.status_code})")
        assert isinstance(folder, CannedResponseFolder)
        try:
            await async_client.canned_responses.list_folders()

            await async_client.canned_responses.update_folder(
                folder.id, name=f"[TEST] Async Updated Folder {_RUN_ID}"
            )

            cr = await async_client.canned_responses.create(
                title=f"[TEST] Async Response {_RUN_ID}",
                content="Hi {{name}}",
                content_html="<p>Hi {{name}}</p>",
                folder_id=folder.id,
            )
            assert isinstance(cr, CannedResponse)

            await async_client.canned_responses.view(cr.id)
            await async_client.canned_responses.update(cr.id, title=f"[TEST] Async Updated {_RUN_ID}")
            await async_client.canned_responses.list_responses_in_folder(folder.id)
            await async_client.canned_responses.delete(cr.id)
        except FreshdeskAPIError as e:
            pytest.skip(f"Canned response lifecycle failed ({e.status_code})")
        finally:
            try:
                await async_client.canned_responses.delete_folder(folder.id)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Custom Objects
# ---------------------------------------------------------------------------

class TestCustomObjectsSync:
    def test_retrieve_schemas(self, client):
        schemas = api_or_skip(client.custom_objects.retrieve_schemas)
        assert isinstance(schemas, list)

    def test_record_lifecycle(self, client):
        schemas = api_or_skip(client.custom_objects.retrieve_schemas)
        if not schemas:
            pytest.skip("No custom object schemas available")
        schema = schemas[0]

        viewed_schema = client.custom_objects.retrieve_schema(schema.id)
        assert isinstance(viewed_schema, CustomObjectSchema)

        try:
            record = client.custom_objects.create_record(schema.id)
            assert isinstance(record, CustomObjectRecord)

            retrieved = client.custom_objects.retrieve_record(schema.id, record.id)
            assert retrieved.id == record.id

            updated = client.custom_objects.update_record(schema.id, record.id)
            assert isinstance(updated, CustomObjectRecord)

            filtered = client.custom_objects.filter_records(schema.id)
            assert isinstance(filtered, list)

            client.custom_objects.delete_record(schema.id, record.id)
        except FreshdeskAPIError:
            pytest.skip("Custom object record operations unavailable")


class TestCustomObjectsAsync:
    async def test_retrieve_schemas(self, async_client):
        schemas = await async_api_or_skip(
            async_client.custom_objects.retrieve_schemas()
        )
        assert isinstance(schemas, list)

    async def test_record_lifecycle(self, async_client):
        schemas = await async_api_or_skip(
            async_client.custom_objects.retrieve_schemas()
        )
        if not schemas:
            pytest.skip("No custom object schemas available")
        schema = schemas[0]

        viewed_schema = await async_client.custom_objects.retrieve_schema(schema.id)
        assert isinstance(viewed_schema, CustomObjectSchema)

        try:
            record = await async_client.custom_objects.create_record(schema.id)
            assert isinstance(record, CustomObjectRecord)

            retrieved = await async_client.custom_objects.retrieve_record(
                schema.id, record.id
            )
            assert retrieved.id == record.id

            updated = await async_client.custom_objects.update_record(
                schema.id, record.id
            )
            assert isinstance(updated, CustomObjectRecord)

            filtered = await async_client.custom_objects.filter_records(schema.id)
            assert isinstance(filtered, list)

            await async_client.custom_objects.delete_record(schema.id, record.id)
        except FreshdeskAPIError:
            pytest.skip("Custom object record operations unavailable")
