"""Mocked unit tests for conversations, filter, solution search, attachments,
pagination, shared rate limiter, base URL and the PEP 561 marker.

No credentials needed: every HTTP call is served by respx.
"""
import importlib.resources
import time

import pytest
import respx
from httpx import Response

from freshdesk import AsyncFreshdesk, Freshdesk, RateLimiter
from freshdesk.models import Attachment, PaginatedList
from freshdesk.models.conversations import Conversation

BASE = "https://testdomain.freshdesk.com/api/v2"
NOW = "2026-01-01T00:00:00Z"
NEXT = {"link": f'<{BASE}/whatever?page=2>; rel="next"'}


def conv(id, ticket_id=7, **extra):
    return {"id": id, "source": 0, "ticket_id": ticket_id, "user_id": 5,
            "created_at": NOW, "updated_at": NOW, **extra}


def ticket(id):
    return {"id": id, "priority": 1, "requester_id": 1, "source": 1, "status": 2,
            "subject": "s", "created_at": NOW, "updated_at": NOW}


def named(id):
    return {"id": id, "name": "n", "created_at": NOW, "updated_at": NOW}


def pages(route):
    return [c.request.url.params.get("page") for c in route.calls]


@pytest.fixture
def fd():
    with Freshdesk("testdomain", "k", max_retries=0, calls_per_minute=0) as c:
        yield c


@pytest.fixture
async def afd():
    async with AsyncFreshdesk("testdomain", "k", max_retries=0, calls_per_minute=0) as c:
        yield c


# ---------------------------------------------------------------------------
# 1. Conversations list + iterator, 5. generic link-header pagination
# ---------------------------------------------------------------------------

class TestConversationsAndPagination:
    @respx.mock
    def test_list_one_page(self, fd):
        route = respx.get(f"{BASE}/tickets/7/conversations").mock(return_value=Response(
            200, json=[conv(1, attachments=[{"id": 9, "name": "a.txt", "file_size": 3}])]
        ))
        result = fd.conversations.list(7, page=2)
        assert pages(route) == ["2"]
        assert isinstance(result[0], Conversation)
        assert isinstance(result[0].attachments[0], Attachment)
        assert result[0].attachments[0].size == 3

    @respx.mock
    def test_iter_all_follows_link_header(self, fd):
        route = respx.get(f"{BASE}/tickets/7/conversations").mock(side_effect=[
            Response(200, json=[conv(1), conv(2)], headers=NEXT),
            Response(200, json=[conv(3)]),
        ])
        assert [c.id for c in fd.conversations.iter_all(7)] == [1, 2, 3]
        assert pages(route) == ["1", "2"]

    @respx.mock
    def test_iteration_is_lazy(self, fd):
        route = respx.get(f"{BASE}/tickets").mock(
            return_value=Response(200, json=[ticket(1)], headers=NEXT)
        )
        assert next(iter(fd.tickets.iter_all())).id == 1
        assert route.call_count == 1

    @respx.mock
    def test_iter_all_keeps_params_and_start_page(self, fd):
        route = respx.get(f"{BASE}/tickets").mock(side_effect=[
            Response(200, json=[ticket(1)], headers=NEXT),
            Response(200, json=[ticket(2)]),
        ])
        ids = [t.id for t in fd.tickets.iter_all(per_page=100, page=3, filter="new_and_my_open")]
        assert ids == [1, 2]
        assert pages(route) == ["3", "4"]
        for call in route.calls:
            assert call.request.url.params["per_page"] == "100"
            assert call.request.url.params["filter"] == "new_and_my_open"

    @respx.mock
    def test_contacts_and_companies_iter_all(self, fd):
        respx.get(f"{BASE}/contacts").mock(return_value=Response(200, json=[named(1)]))
        respx.get(f"{BASE}/companies").mock(return_value=Response(200, json=[named(2)]))
        assert [c.id for c in fd.contacts.iter_all()] == [1]
        assert [c.id for c in fd.companies.iter_all()] == [2]

    @respx.mock
    async def test_async_list_and_iter_all(self, afd):
        route = respx.get(f"{BASE}/tickets/7/conversations").mock(side_effect=[
            Response(200, json=[conv(1)]),
            Response(200, json=[conv(1)], headers=NEXT),
            Response(200, json=[conv(2)]),
        ])
        assert [c.id for c in await afd.conversations.list(7)] == [1]
        assert [c.id async for c in afd.conversations.iter_all(7)] == [1, 2]
        assert pages(route) == [None, "1", "2"]


# ---------------------------------------------------------------------------
# 2. filter(): quoted query, %20 encoding, page, total
# ---------------------------------------------------------------------------

class TestFilter:
    @respx.mock
    def test_ticket_filter_quotes_query_and_returns_total(self, fd):
        route = respx.get(f"{BASE}/search/tickets").mock(
            return_value=Response(200, json={"total": 31, "results": [ticket(1)]})
        )
        res = fd.tickets.filter("status:2 AND priority:3", page=2)
        url = route.calls.last.request.url
        assert url.params["query"] == '"status:2 AND priority:3"'
        assert url.params["page"] == "2"
        assert b"%22status%3A2%20AND%20priority%3A3%22" in url.raw_path
        assert isinstance(res, PaginatedList)
        assert res.total == 31
        assert res.items[0].id == 1

    @respx.mock
    def test_already_quoted_query_is_not_wrapped_twice(self, fd):
        route = respx.get(f"{BASE}/search/contacts").mock(
            return_value=Response(200, json={"total": 0, "results": []})
        )
        res = fd.contacts.filter('  "email:\'a@b.com\'"  ')
        assert route.calls.last.request.url.params["query"] == '"email:\'a@b.com\'"'
        assert "page" not in route.calls.last.request.url.params
        assert res.total == 0 and res.items == []

    @respx.mock
    async def test_async_company_filter(self, afd):
        route = respx.get(f"{BASE}/search/companies").mock(
            return_value=Response(200, json={"total": 1, "results": [named(4)]})
        )
        res = await afd.companies.filter("domain:'x.com'", page=10)
        assert route.calls.last.request.url.params["query"] == "\"domain:'x.com'\""
        assert res.total == 1 and res.items[0].id == 4

    @pytest.mark.parametrize("page", [0, 11])
    def test_page_out_of_range(self, fd, page):
        with pytest.raises(ValueError, match="between 1 and 10"):
            fd.tickets.filter("status:2", page=page)


# ---------------------------------------------------------------------------
# 3. Solution article search uses term=
# ---------------------------------------------------------------------------

class TestSolutionSearch:
    @respx.mock
    def test_search_articles_sends_term(self, fd):
        route = respx.get(f"{BASE}/search/solutions").mock(
            return_value=Response(200, json=[{"id": 2, "title": "t", "description": "d", "status": 2,
                                     "folder_id": 4, "created_at": NOW, "updated_at": NOW}])
        )
        res = fd.solutions.search_articles("sample")
        params = route.calls.last.request.url.params
        assert params["term"] == "sample" and "keyword" not in params
        assert res[0].id == 2

    @respx.mock
    async def test_async_search_articles_sends_term(self, afd):
        route = respx.get(f"{BASE}/search/solutions").mock(return_value=Response(200, json=[]))
        await afd.solutions.search_articles(term="sample")
        assert route.calls.last.request.url.params["term"] == "sample"


# ---------------------------------------------------------------------------
# 4. Attachments: multipart uploads and typed model
# ---------------------------------------------------------------------------

class TestAttachments:
    @respx.mock
    def test_note_with_attachment_is_multipart(self, fd):
        route = respx.post(f"{BASE}/tickets/7/notes").mock(
            return_value=Response(201, json=conv(1, private=True))
        )
        fd.conversations.create_note(
            7, body="see log", private=True, notify_emails=["a@x.com"],
            attachments=[("log.txt", b"hello", "text/plain")],
        )
        req = route.calls.last.request
        assert req.headers["Content-Type"].startswith("multipart/form-data; boundary=")
        body = req.read()
        assert b'name="attachments[]"; filename="log.txt"' in body
        assert b"hello" in body
        assert b'name="body"\r\n\r\nsee log' in body
        assert b'name="private"\r\n\r\ntrue' in body
        assert b'name="notify_emails[]"\r\n\r\na@x.com' in body

    @respx.mock
    def test_ticket_with_attachment_sends_custom_fields_as_form_keys(self, fd):
        route = respx.post(f"{BASE}/tickets").mock(return_value=Response(201, json=ticket(1)))
        fd.tickets.create(
            subject="s", custom_fields={"cf_env": "prod"},
            attachments=[("a.bin", b"\x00\x01")],
        )
        body = route.calls.last.request.read()
        assert b'name="custom_fields[cf_env]"\r\n\r\nprod' in body

    @respx.mock
    def test_json_requests_keep_json_content_type(self, fd):
        create = respx.post(f"{BASE}/tickets").mock(return_value=Response(201, json=ticket(1)))
        restore = respx.put(f"{BASE}/tickets/1/restore").mock(return_value=Response(204))
        fd.tickets.create(subject="s", priority=1)
        fd.tickets.restore(1)
        assert create.calls.last.request.headers["Content-Type"] == "application/json"
        assert create.calls.last.request.read() == b'{"subject":"s","priority":1}'
        assert restore.calls.last.request.headers["Content-Type"] == "application/json"

    @respx.mock
    async def test_async_reply_with_attachment(self, afd):
        route = respx.post(f"{BASE}/tickets/7/reply").mock(
            return_value=Response(201, json=conv(1))
        )
        await afd.conversations.create_reply(7, body="hi", attachments=[("x.txt", b"x")])
        assert route.calls.last.request.headers["Content-Type"].startswith("multipart/form-data")

    def test_attachment_model_reads_size_and_file_size(self):
        a = Attachment.model_validate({
            "id": 1, "name": "a.jpg", "content_type": "image/jpeg", "size": 98,
            "attachment_url": "https://cdn/x", "thumb_url": "https://cdn/t",
            "created_at": NOW, "updated_at": NOW,
        })
        b = Attachment.model_validate({"id": 2, "file_size": 44115})
        assert (a.size, a.thumb_url, b.size) == (98, "https://cdn/t", 44115)


# ---------------------------------------------------------------------------
# 6. PEP 561 marker
# ---------------------------------------------------------------------------

def test_py_typed_marker_is_in_package():
    assert importlib.resources.files("freshdesk").joinpath("py.typed").is_file()


# ---------------------------------------------------------------------------
# 7. Shared rate limiter
# ---------------------------------------------------------------------------

class TestSharedRateLimiter:
    @respx.mock
    async def test_clients_share_one_limiter(self):
        respx.get(f"{BASE}/tickets/1").mock(return_value=Response(200, json=ticket(1)))
        limiter = RateLimiter(5000, window=3600)
        a = Freshdesk("testdomain", "user-a", rate_limiter=limiter)
        b = Freshdesk("testdomain", "user-b", rate_limiter=limiter, calls_per_minute=10)
        c = AsyncFreshdesk("testdomain", "user-c", rate_limiter=limiter)
        a.tickets.view(1)
        b.tickets.view(1)
        await c.tickets.view(1)
        assert a.rate_limiter is b.rate_limiter is c.rate_limiter is limiter
        assert limiter.current_usage == 3
        a.close()
        b.close()
        await c.close()

    def test_default_limiter_is_per_client_growth_plan(self):
        a, b = Freshdesk("d", "k"), Freshdesk("d", "k")
        assert a.rate_limiter is not b.rate_limiter
        assert a.rate_limiter.calls_per_minute == 200
        assert a.rate_limiter.window == 60.0

    def test_window_controls_eviction(self):
        hourly, minutely = RateLimiter(10, window=3600), RateLimiter(10)
        for limiter in (hourly, minutely):
            limiter._timestamps.append(time.monotonic() - 120)
        assert hourly.current_usage == 1
        assert minutely.current_usage == 0


# ---------------------------------------------------------------------------
# 8. Configurable base URL
# ---------------------------------------------------------------------------

class TestBaseUrl:
    def test_default_base_url(self):
        assert Freshdesk("innovatrics", "k").base_url == "https://innovatrics.freshdesk.com/api/v2/"

    @respx.mock
    def test_custom_base_url_is_used_for_every_page(self):
        proxy = "https://proxy.example.com/fd/api/v2"
        route = respx.get(f"{proxy}/tickets").mock(side_effect=[
            Response(200, json=[ticket(1)],
                     headers={"link": '<https://other.example.com/api/v2/tickets?page=2>; rel="next"'}),
            Response(200, json=[ticket(2)]),
        ])
        with Freshdesk("innovatrics", "k", base_url=proxy, calls_per_minute=0) as c:
            assert c.base_url == proxy + "/"
            assert [t.id for t in c.tickets.iter_all()] == [1, 2]
        # The next-page host from the link header is never contacted.
        assert {call.request.url.host for call in route.calls} == {"proxy.example.com"}

    @respx.mock
    async def test_async_custom_base_url(self):
        route = respx.get("https://fd.local/api/v2/tickets/1").mock(
            return_value=Response(200, json=ticket(1))
        )
        async with AsyncFreshdesk("x", "k", base_url="https://fd.local/api/v2/", calls_per_minute=0) as c:
            await c.tickets.view(1)
        assert route.called


# ---------------------------------------------------------------------------
# Fixes ported from abaskin/freshdesk-lib (90f72b7)
# ---------------------------------------------------------------------------

class TestPortedFixes:
    @respx.mock
    def test_company_autocomplete_reads_companies_key(self, fd):
        respx.get(f"{BASE}/companies/autocomplete").mock(return_value=Response(
            200, json={"companies": [{"id": 1, "name": "Acme"}]}
        ))
        res = fd.companies.search("Acme")
        assert [(c.id, c.name, c.created_at) for c in res] == [(1, "Acme", None)]

    @respx.mock
    async def test_async_company_autocomplete(self, afd):
        respx.get(f"{BASE}/companies/autocomplete").mock(
            return_value=Response(200, json={"companies": []})
        )
        assert await afd.companies.search("x") == []

    def test_conversation_accepts_null_emails_and_user(self):
        c = Conversation.model_validate(
            conv(1, to_emails=None, cc_emails=None, bcc_emails=None, user_id=None)
        )
        assert c.to_emails is None and c.user_id is None

    @respx.mock
    def test_get_associated(self, fd):
        respx.get(f"{BASE}/tickets/20/associated_tickets").mock(
            return_value=Response(200, json={"tickets": [ticket(44)]})
        )
        respx.get(f"{BASE}/tickets/21/associated_tickets").mock(
            return_value=Response(404, json={})
        )
        assert [t.id for t in fd.tickets.get_associated(20)] == [44]
        assert fd.tickets.get_associated(21) == []

    @respx.mock
    async def test_async_get_associated_reraises_other_errors(self, afd):
        from freshdesk.exceptions import FreshdeskAPIError
        respx.get(f"{BASE}/tickets/20/associated_tickets").mock(
            return_value=Response(500, json={})
        )
        with pytest.raises(FreshdeskAPIError):
            await afd.tickets.get_associated(20)



def test_null_lists_become_empty_lists():
    from freshdesk.models.tickets import Ticket
    ticket = Ticket.model_validate({
        "id": 1, "priority": 1, "requester_id": 2, "source": 1, "status": 2, "subject": "s",
        "created_at": "2020-01-01T00:00:00Z", "updated_at": "2020-01-01T00:00:00Z",
        "reply_cc_emails": None, "cc_emails": None, "fwd_emails": None, "tags": None,
    })
    assert (ticket.reply_cc_emails, ticket.cc_emails, ticket.fwd_emails, ticket.tags) == ([], [], [], [])
