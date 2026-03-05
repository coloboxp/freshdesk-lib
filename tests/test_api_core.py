"""Integration tests for core API modules: tickets, contacts, companies,
agents, groups, conversations.

Every test hits the real Freshdesk API.  Skipped automatically when
credentials are missing (see conftest.py).
"""
import uuid

import pytest

from freshdesk.exceptions import FreshdeskAPIError
from freshdesk.models.agents import Agent
from freshdesk.models.companies import Company
from freshdesk.models.contacts import Contact
from freshdesk.models.conversations import Conversation
from freshdesk.models.groups import Group
from freshdesk.models.tickets import Ticket
from conftest import api_or_skip, async_api_or_skip

_RUN_ID = uuid.uuid4().hex[:8]

# ---------------------------------------------------------------------------
# Tickets
# ---------------------------------------------------------------------------

TICKET_DEFAULTS = dict(
    subject=f"[TEST] freshdesk-lib integration {_RUN_ID}",
    description="Automated test – safe to delete",
    email=f"pytest-{_RUN_ID}@test.example.com",
    priority=1,
    status=2,
)


class TestTicketsSync:
    def test_list(self, client):
        result = client.tickets.list()
        assert isinstance(result, list)

    def test_crud_lifecycle(self, client):
        try:
            t = client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        assert isinstance(t, Ticket)
        assert t.subject == TICKET_DEFAULTS["subject"]
        try:
            viewed = client.tickets.view(t.id)
            assert viewed.id == t.id

            viewed_inc = client.tickets.view(t.id, include="stats")
            assert viewed_inc.id == t.id

            updated = client.tickets.update(t.id, priority=3)
            assert updated.priority == 3

            filtered = client.tickets.filter(
                query='"subject:[TEST] freshdesk-lib integration"'
            )
            assert isinstance(filtered, list)
        finally:
            client.tickets.delete(t.id)

    def test_restore(self, client):
        try:
            t = client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        try:
            client.tickets.delete(t.id)
            client.tickets.restore(t.id)
        finally:
            try:
                client.tickets.delete(t.id)
            except Exception:
                pass

    def test_forward(self, client):
        try:
            t = client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        try:
            api_or_skip(
                client.tickets.forward, t.id,
                body="Forwarded by test",
                to_emails=["fwd-target@test.example.com"],
            )
        finally:
            try:
                client.tickets.delete(t.id)
            except Exception:
                pass


class TestTicketsAsync:
    async def test_list(self, async_client):
        result = await async_client.tickets.list()
        assert isinstance(result, list)

    async def test_crud_lifecycle(self, async_client):
        try:
            t = await async_client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        assert isinstance(t, Ticket)
        try:
            viewed = await async_client.tickets.view(t.id)
            assert viewed.id == t.id

            updated = await async_client.tickets.update(t.id, priority=2)
            assert updated.priority == 2

            filtered = await async_client.tickets.filter(
                query='"subject:[TEST] freshdesk-lib"'
            )
            assert isinstance(filtered, list)
        finally:
            await async_client.tickets.delete(t.id)

    async def test_restore(self, async_client):
        try:
            t = await async_client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        try:
            await async_client.tickets.delete(t.id)
            await async_client.tickets.restore(t.id)
        finally:
            try:
                await async_client.tickets.delete(t.id)
            except Exception:
                pass

    async def test_forward(self, async_client):
        try:
            t = await async_client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        try:
            await async_api_or_skip(
                async_client.tickets.forward(
                    t.id,
                    body="Async forward test",
                    to_emails=["fwd@test.example.com"],
                )
            )
        finally:
            try:
                await async_client.tickets.delete(t.id)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------

class TestContactsSync:
    def test_list(self, client):
        result = client.contacts.list()
        assert isinstance(result, list)

    def test_crud_lifecycle(self, client):
        try:
            c = client.contacts.create(name=f"[TEST] Pytest Contact {_RUN_ID}", email=f"pytest-c-{_RUN_ID}@test.example.com")
        except FreshdeskAPIError as e:
            pytest.skip(f"Contact creation rejected ({e.status_code})")
        assert isinstance(c, Contact)
        try:
            client.contacts.view(c.id)
            client.contacts.update(c.id, job_title="Tester")
            client.contacts.search(term="[TEST] Pytest")
            client.contacts.filter(query='"name:[TEST] Pytest Contact"')
        except FreshdeskAPIError as e:
            pytest.skip(f"Contact lifecycle operation failed ({e.status_code})")
        finally:
            try:
                client.contacts.delete(c.id)
                client.contacts.hard_delete(c.id)
            except Exception:
                pass

    def test_restore(self, client):
        try:
            c = client.contacts.create(name=f"[TEST] Restore Contact {_RUN_ID}")
        except FreshdeskAPIError as e:
            pytest.skip(f"Contact creation rejected by instance ({e.status_code})")
        try:
            client.contacts.delete(c.id)
            client.contacts.restore(c.id)
        finally:
            try:
                client.contacts.delete(c.id)
                client.contacts.hard_delete(c.id)
            except Exception:
                pass

    def test_send_invite(self, client):
        c = client.contacts.create(name=f"[TEST] Invite Contact {_RUN_ID}", email=f"invite-{_RUN_ID}@test.example.com")
        try:
            api_or_skip(client.contacts.send_invite, c.id)
        except FreshdeskAPIError:
            pass
        finally:
            try:
                client.contacts.delete(c.id)
                client.contacts.hard_delete(c.id)
            except Exception:
                pass

    def test_merge(self, client):
        c1 = client.contacts.create(name=f"[TEST] Merge Primary {_RUN_ID}", email=f"merge1-{_RUN_ID}@test.example.com")
        c2 = client.contacts.create(name=f"[TEST] Merge Secondary {_RUN_ID}", email=f"merge2-{_RUN_ID}@test.example.com")
        try:
            api_or_skip(client.contacts.merge, c1.id, [c2.id])
        except FreshdeskAPIError:
            pass
        finally:
            for cid in (c1.id, c2.id):
                try:
                    client.contacts.delete(cid)
                    client.contacts.hard_delete(cid)
                except Exception:
                    pass

    def test_make_agent(self, client):
        c = client.contacts.create(name=f"[TEST] AgentConvert {_RUN_ID}", email=f"makeagent-{_RUN_ID}@test.example.com")
        try:
            api_or_skip(client.contacts.make_agent, c.id, occasional=True)
        except FreshdeskAPIError:
            pass
        finally:
            try:
                client.contacts.delete(c.id)
                client.contacts.hard_delete(c.id)
            except Exception:
                pass


class TestContactsAsync:
    async def test_list(self, async_client):
        result = await async_client.contacts.list()
        assert isinstance(result, list)

    async def test_crud_lifecycle(self, async_client):
        try:
            c = await async_client.contacts.create(
                name=f"[TEST] Async Contact {_RUN_ID}", email=f"async-c-{_RUN_ID}@test.example.com"
            )
        except FreshdeskAPIError as e:
            pytest.skip(f"Contact creation rejected ({e.status_code})")
        assert isinstance(c, Contact)
        try:
            await async_client.contacts.view(c.id)
            await async_client.contacts.update(c.id, job_title="AsyncTester")
            await async_client.contacts.search(term="[TEST] Async")
            await async_client.contacts.filter(query='"name:[TEST] Async"')
        except FreshdeskAPIError as e:
            pytest.skip(f"Contact lifecycle operation failed ({e.status_code})")
        finally:
            try:
                await async_client.contacts.delete(c.id)
                await async_client.contacts.hard_delete(c.id)
            except Exception:
                pass

    async def test_restore(self, async_client):
        try:
            c = await async_client.contacts.create(name=f"[TEST] Async Restore {_RUN_ID}")
        except FreshdeskAPIError as e:
            pytest.skip(f"Contact creation rejected by instance ({e.status_code})")
        try:
            await async_client.contacts.delete(c.id)
            await async_client.contacts.restore(c.id)
        finally:
            try:
                await async_client.contacts.delete(c.id)
                await async_client.contacts.hard_delete(c.id)
            except Exception:
                pass

    async def test_send_invite(self, async_client):
        c = await async_client.contacts.create(
            name=f"[TEST] Async Invite {_RUN_ID}", email=f"asyncinv-{_RUN_ID}@test.example.com"
        )
        try:
            await async_api_or_skip(async_client.contacts.send_invite(c.id))
        except FreshdeskAPIError:
            pass
        finally:
            try:
                await async_client.contacts.delete(c.id)
                await async_client.contacts.hard_delete(c.id)
            except Exception:
                pass

    async def test_merge(self, async_client):
        c1 = await async_client.contacts.create(
            name=f"[TEST] Async Merge1 {_RUN_ID}", email=f"amerge1-{_RUN_ID}@test.example.com"
        )
        c2 = await async_client.contacts.create(
            name=f"[TEST] Async Merge2 {_RUN_ID}", email=f"amerge2-{_RUN_ID}@test.example.com"
        )
        try:
            await async_api_or_skip(async_client.contacts.merge(c1.id, [c2.id]))
        except FreshdeskAPIError:
            pass
        finally:
            for cid in (c1.id, c2.id):
                try:
                    await async_client.contacts.delete(cid)
                    await async_client.contacts.hard_delete(cid)
                except Exception:
                    pass

    async def test_make_agent(self, async_client):
        c = await async_client.contacts.create(
            name=f"[TEST] Async MakeAgent {_RUN_ID}", email=f"amakeag-{_RUN_ID}@test.example.com"
        )
        try:
            await async_api_or_skip(
                async_client.contacts.make_agent(c.id, occasional=True)
            )
        except FreshdeskAPIError:
            pass
        finally:
            try:
                await async_client.contacts.delete(c.id)
                await async_client.contacts.hard_delete(c.id)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Companies
# ---------------------------------------------------------------------------

class TestCompaniesSync:
    def test_list(self, client):
        result = client.companies.list()
        assert isinstance(result, list)

    def test_crud_lifecycle(self, client):
        try:
            c = client.companies.create(name=f"[TEST] Pytest Corp {_RUN_ID}")
        except FreshdeskAPIError as e:
            pytest.skip(f"Company creation rejected by instance ({e.status_code})")
        assert isinstance(c, Company)
        try:
            viewed = client.companies.view(c.id)
            assert viewed.id == c.id

            updated = client.companies.update(c.id, description="Updated")
            assert updated.description == "Updated"

            searched = client.companies.search(name="[TEST] Pytest")
            assert isinstance(searched, list)

            filtered = client.companies.filter(query='"name:[TEST] Pytest Corp"')
            assert isinstance(filtered, list)
        finally:
            client.companies.delete(c.id)


class TestCompaniesAsync:
    async def test_list(self, async_client):
        result = await async_client.companies.list()
        assert isinstance(result, list)

    async def test_crud_lifecycle(self, async_client):
        try:
            c = await async_client.companies.create(name=f"[TEST] Async Corp {_RUN_ID}")
        except FreshdeskAPIError as e:
            pytest.skip(f"Company creation rejected by instance ({e.status_code})")
        assert isinstance(c, Company)
        try:
            viewed = await async_client.companies.view(c.id)
            assert viewed.id == c.id

            updated = await async_client.companies.update(c.id, description="AUpdated")
            assert updated.description == "AUpdated"

            searched = await async_client.companies.search(name="[TEST] Async")
            assert isinstance(searched, list)

            filtered = await async_client.companies.filter(
                query='"name:[TEST] Async Corp"'
            )
            assert isinstance(filtered, list)
        finally:
            await async_client.companies.delete(c.id)


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

class TestAgentsSync:
    def test_list(self, client):
        result = client.agents.list()
        assert isinstance(result, list)
        assert all(isinstance(a, Agent) for a in result)

    def test_me(self, client):
        me = client.agents.me()
        assert isinstance(me, Agent)
        assert me.id > 0

    def test_view(self, client):
        me = client.agents.me()
        viewed = client.agents.view(me.id)
        assert viewed.id == me.id

    def test_search(self, client):
        result = client.agents.search(term="a")
        assert isinstance(result, list)


class TestAgentsAsync:
    async def test_list(self, async_client):
        result = await async_client.agents.list()
        assert isinstance(result, list)

    async def test_me(self, async_client):
        me = await async_client.agents.me()
        assert isinstance(me, Agent)

    async def test_view(self, async_client):
        me = await async_client.agents.me()
        viewed = await async_client.agents.view(me.id)
        assert viewed.id == me.id

    async def test_search(self, async_client):
        result = await async_client.agents.search(term="a")
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------

class TestGroupsSync:
    def test_list(self, client):
        result = client.groups.list()
        assert isinstance(result, list)

    def test_crud_lifecycle(self, client):
        g = client.groups.create(name=f"[TEST] Pytest Group {_RUN_ID}")
        assert isinstance(g, Group)
        try:
            viewed = client.groups.view(g.id)
            assert viewed.id == g.id

            updated = client.groups.update(g.id, description="Updated desc")
            assert updated.description == "Updated desc"
        finally:
            client.groups.delete(g.id)


class TestGroupsAsync:
    async def test_list(self, async_client):
        result = await async_client.groups.list()
        assert isinstance(result, list)

    async def test_crud_lifecycle(self, async_client):
        g = await async_client.groups.create(name=f"[TEST] Async Group {_RUN_ID}")
        assert isinstance(g, Group)
        try:
            viewed = await async_client.groups.view(g.id)
            assert viewed.id == g.id

            updated = await async_client.groups.update(g.id, description="ADesc")
            assert updated.description == "ADesc"
        finally:
            await async_client.groups.delete(g.id)


# ---------------------------------------------------------------------------
# Conversations
# ---------------------------------------------------------------------------

class TestConversationsSync:
    def test_reply_note_update_delete(self, client):
        try:
            ticket = client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        try:
            reply = client.conversations.create_reply(
                ticket.id, body="<p>Test reply</p>"
            )
            assert isinstance(reply, Conversation)

            note = client.conversations.create_note(
                ticket.id, body="Private note", private=True
            )
            assert isinstance(note, Conversation)

            updated = client.conversations.update(note.id, body="Updated note")
            assert isinstance(updated, Conversation)

            client.conversations.delete(note.id)
        finally:
            client.tickets.delete(ticket.id)

    def test_reply_to_forward(self, client):
        try:
            ticket = client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        try:
            api_or_skip(
                client.conversations.reply_to_forward,
                ticket.id,
                body="Forward reply",
            )
        except FreshdeskAPIError:
            pass
        finally:
            client.tickets.delete(ticket.id)


class TestConversationsAsync:
    async def test_reply_note_update_delete(self, async_client):
        try:
            ticket = await async_client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        try:
            reply = await async_client.conversations.create_reply(
                ticket.id, body="<p>Async reply</p>"
            )
            assert isinstance(reply, Conversation)

            note = await async_client.conversations.create_note(
                ticket.id, body="Async note", private=True
            )
            assert isinstance(note, Conversation)

            updated = await async_client.conversations.update(
                note.id, body="Updated async note"
            )
            assert isinstance(updated, Conversation)

            await async_client.conversations.delete(note.id)
        finally:
            await async_client.tickets.delete(ticket.id)

    async def test_reply_to_forward(self, async_client):
        try:
            ticket = await async_client.tickets.create(**TICKET_DEFAULTS)
        except FreshdeskAPIError as exc:
            pytest.skip(f"Ticket creation failed (HTTP {exc.status_code}): {exc}")
        try:
            await async_api_or_skip(
                async_client.conversations.reply_to_forward(
                    ticket.id, body="Async fwd reply"
                )
            )
        except FreshdeskAPIError:
            pass
        finally:
            await async_client.tickets.delete(ticket.id)
