"""Tests for Freshdesk / AsyncFreshdesk client behaviour.

Section 1 – Mocked unit tests (always run, no credentials needed).
Section 2 – Integration tests (require real credentials via config fixture).
"""
import pytest
import respx
from httpx import Response

from freshdesk import AsyncFreshdesk, Freshdesk
from freshdesk.exceptions import (
    FreshdeskAPIError,
    FreshdeskAuthError,
    FreshdeskRateLimitError,
)

BASE = "https://testdomain.freshdesk.com/api/v2"

# ───────────────────────────────────────────────────────────────────────────
# Fixtures (mocked clients)
# ───────────────────────────────────────────────────────────────────────────

@pytest.fixture
def sync_client():
    return Freshdesk(domain="testdomain", api_key="testkey", max_retries=1, calls_per_minute=0)


@pytest.fixture
async def mock_async_client():
    async with AsyncFreshdesk(domain="testdomain", api_key="testkey", max_retries=1, calls_per_minute=0) as c:
        yield c


# ═══════════════════════════════════════════════════════════════════════════
# Section 1 – Mocked (unit) tests
# ═══════════════════════════════════════════════════════════════════════════

class TestSyncClientMocked:
    """Sync client behaviour with mocked HTTP."""

    @respx.mock
    def test_success_json(self, sync_client):
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(200, json=[{"id": 1}])
        )
        assert sync_client.request("GET", "tickets") == [{"id": 1}]

    @respx.mock
    def test_204_returns_none(self, sync_client):
        respx.delete(f"{BASE}/tickets/1").mock(return_value=Response(204))
        assert sync_client.request("DELETE", "tickets/1") is None

    @respx.mock
    def test_non_json_response(self, sync_client):
        respx.get(f"{BASE}/export").mock(
            return_value=Response(
                200, content=b"BINARYDATA",
                headers={"Content-Type": "application/octet-stream"},
            )
        )
        assert sync_client.request("GET", "export") == b"BINARYDATA"

    @respx.mock
    def test_auth_error_401(self, sync_client):
        respx.get(f"{BASE}/tickets").mock(return_value=Response(401))
        with pytest.raises(FreshdeskAuthError):
            sync_client.request("GET", "tickets")

    @respx.mock
    def test_auth_error_403(self, sync_client):
        respx.get(f"{BASE}/tickets").mock(return_value=Response(403))
        with pytest.raises(FreshdeskAuthError):
            sync_client.request("GET", "tickets")

    @respx.mock
    def test_rate_limit_retries_exhausted(self, sync_client):
        route = respx.get(f"{BASE}/tickets").mock(
            return_value=Response(429, headers={"Retry-After": "0"})
        )
        with pytest.raises(FreshdeskRateLimitError) as exc_info:
            sync_client.request("GET", "tickets")
        assert exc_info.value.retry_after == 0
        assert route.call_count == 2  # initial + 1 retry

    @respx.mock
    def test_api_error_json_payload(self, sync_client):
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(400, json={"description": "Validation failed"})
        )
        with pytest.raises(FreshdeskAPIError) as exc_info:
            sync_client.request("GET", "tickets")
        assert exc_info.value.status_code == 400
        assert exc_info.value.error_payload == {"description": "Validation failed"}

    @respx.mock
    def test_api_error_non_json_body(self, sync_client):
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        with pytest.raises(FreshdeskAPIError) as exc_info:
            sync_client.request("GET", "tickets")
        assert exc_info.value.status_code == 500
        assert exc_info.value.error_payload == {"text": "Internal Server Error"}

    def test_context_manager(self):
        with Freshdesk(domain="testdomain", api_key="k") as c:
            assert isinstance(c, Freshdesk)
            assert c.base_url == f"{BASE}/"

    def test_close(self):
        c = Freshdesk(domain="testdomain", api_key="k")
        c.close()

    def test_api_sub_resources_attached(self, sync_client):
        assert hasattr(sync_client, "tickets")
        assert hasattr(sync_client, "contacts")
        assert hasattr(sync_client, "agents")
        assert hasattr(sync_client, "admin")


class TestAsyncClientMocked:
    """Async client behaviour with mocked HTTP."""

    @respx.mock
    async def test_success_json(self, mock_async_client):
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(200, json=[{"id": 1}])
        )
        assert await mock_async_client.request("GET", "tickets") == [{"id": 1}]

    @respx.mock
    async def test_204_returns_none(self, mock_async_client):
        respx.delete(f"{BASE}/tickets/1").mock(return_value=Response(204))
        assert await mock_async_client.request("DELETE", "tickets/1") is None

    @respx.mock
    async def test_non_json_response(self, mock_async_client):
        respx.get(f"{BASE}/export").mock(
            return_value=Response(
                200, content=b"BIN",
                headers={"Content-Type": "application/octet-stream"},
            )
        )
        assert await mock_async_client.request("GET", "export") == b"BIN"

    @respx.mock
    async def test_auth_error(self, mock_async_client):
        respx.get(f"{BASE}/tickets").mock(return_value=Response(401))
        with pytest.raises(FreshdeskAuthError):
            await mock_async_client.request("GET", "tickets")

    @respx.mock
    async def test_rate_limit(self, mock_async_client):
        route = respx.get(f"{BASE}/tickets").mock(
            return_value=Response(429, headers={"Retry-After": "0"})
        )
        with pytest.raises(FreshdeskRateLimitError):
            await mock_async_client.request("GET", "tickets")
        assert route.call_count == 2

    @respx.mock
    async def test_api_error(self, mock_async_client):
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(422, json={"errors": ["invalid"]})
        )
        with pytest.raises(FreshdeskAPIError) as exc_info:
            await mock_async_client.request("GET", "tickets")
        assert exc_info.value.status_code == 422

    @respx.mock
    async def test_api_error_non_json(self, mock_async_client):
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(502, text="Bad Gateway")
        )
        with pytest.raises(FreshdeskAPIError) as exc_info:
            await mock_async_client.request("GET", "tickets")
        assert exc_info.value.error_payload == {"text": "Bad Gateway"}

    async def test_context_manager(self):
        async with AsyncFreshdesk(domain="testdomain", api_key="k") as c:
            assert isinstance(c, AsyncFreshdesk)

    async def test_close(self):
        c = AsyncFreshdesk(domain="testdomain", api_key="k")
        await c.close()

    async def test_api_sub_resources_attached(self, mock_async_client):
        assert hasattr(mock_async_client, "tickets")
        assert hasattr(mock_async_client, "contacts")
        assert hasattr(mock_async_client, "admin")


# ═══════════════════════════════════════════════════════════════════════════
# Section 2 – Integration tests (real Freshdesk instance)
# ═══════════════════════════════════════════════════════════════════════════

class TestSyncClientIntegration:
    """Real HTTP calls – skipped when no credentials are available."""

    def test_init_and_base_url(self, config):
        c = Freshdesk(domain=config["domain"], api_key=config["api_key"])
        assert config["domain"] in c.base_url
        c.close()

    def test_context_manager_real(self, config):
        with Freshdesk(domain=config["domain"], api_key=config["api_key"]) as c:
            result = c.request("GET", "tickets")
            assert isinstance(result, list)

    def test_request_returns_list(self, client):
        result = client.request("GET", "tickets")
        assert isinstance(result, list)


class TestAsyncClientIntegration:

    async def test_context_manager_real(self, config):
        async with AsyncFreshdesk(
            domain=config["domain"], api_key=config["api_key"]
        ) as c:
            result = await c.request("GET", "tickets")
            assert isinstance(result, list)

    async def test_request_returns_list(self, async_client):
        result = await async_client.request("GET", "tickets")
        assert isinstance(result, list)
