"""Tests for logging utilities and log output from client / rate limiter."""
import logging

import pytest
import respx
from httpx import Response

from freshdesk import (
    AsyncFreshdesk,
    CallbackHandler,
    Freshdesk,
    enable_logging,
)

BASE = "https://testdomain.freshdesk.com/api/v2"


# ---------------------------------------------------------------------------
# enable_logging
# ---------------------------------------------------------------------------

class TestEnableLogging:
    def test_attaches_handler(self):
        handler = enable_logging(level="warning")
        try:
            lg = logging.getLogger("freshdesk")
            assert handler in lg.handlers
        finally:
            lg.removeHandler(handler)

    def test_returns_handler(self):
        handler = enable_logging(level=logging.INFO)
        try:
            assert isinstance(handler, logging.StreamHandler)
        finally:
            logging.getLogger("freshdesk").removeHandler(handler)

    def test_int_level(self):
        handler = enable_logging(level=logging.DEBUG)
        try:
            assert handler.level == logging.DEBUG
        finally:
            logging.getLogger("freshdesk").removeHandler(handler)


# ---------------------------------------------------------------------------
# CallbackHandler
# ---------------------------------------------------------------------------

class TestCallbackHandler:
    def test_receives_records(self):
        records = []
        handler = CallbackHandler(records.append)
        lg = logging.getLogger("freshdesk.test_callback")
        lg.addHandler(handler)
        lg.setLevel(logging.DEBUG)
        try:
            lg.info("hello %s", "world")
            assert len(records) == 1
            assert records[0].getMessage() == "hello world"
            assert records[0].levelname == "INFO"
        finally:
            lg.removeHandler(handler)

    def test_string_level(self):
        handler = CallbackHandler(lambda r: None, level="error")
        assert handler.level == logging.ERROR

    def test_callback_exception_handled(self):
        def bad_callback(record):
            raise RuntimeError("boom")

        handler = CallbackHandler(bad_callback)
        lg = logging.getLogger("freshdesk.test_bad_cb")
        lg.addHandler(handler)
        lg.setLevel(logging.DEBUG)
        try:
            lg.info("this should not raise")
        finally:
            lg.removeHandler(handler)


# ---------------------------------------------------------------------------
# Client logging – mocked
# ---------------------------------------------------------------------------

class TestClientLogging:
    @respx.mock
    def test_request_logs_debug(self, caplog):
        c = Freshdesk(domain="testdomain", api_key="k", calls_per_minute=0)
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(200, json=[])
        )
        with caplog.at_level(logging.DEBUG, logger="freshdesk"):
            c.request("GET", "tickets")
        messages = [r.message for r in caplog.records]
        assert any("→ GET tickets" in m for m in messages)
        assert any("← 200 GET tickets" in m for m in messages)
        c.close()

    @respx.mock
    def test_error_logs_error(self, caplog):
        c = Freshdesk(domain="testdomain", api_key="k", calls_per_minute=0)
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(400, json={"error": "bad"})
        )
        with caplog.at_level(logging.ERROR, logger="freshdesk"):
            with pytest.raises(Exception):
                c.request("GET", "tickets")
        assert any(r.levelname == "ERROR" for r in caplog.records)
        c.close()

    @respx.mock
    def test_rate_limit_logs_warning(self, caplog):
        c = Freshdesk(domain="testdomain", api_key="k", max_retries=0, calls_per_minute=0)
        respx.get(f"{BASE}/tickets").mock(
            return_value=Response(429, headers={"Retry-After": "1"})
        )
        with caplog.at_level(logging.WARNING, logger="freshdesk"):
            with pytest.raises(Exception):
                c.request("GET", "tickets")
        assert any("Rate limit" in r.message for r in caplog.records)
        c.close()

    def test_init_logs_info(self, caplog):
        with caplog.at_level(logging.INFO, logger="freshdesk"):
            c = Freshdesk(domain="testdomain", api_key="k", plan="pro")
        assert any("Initialized" in r.message and "pro" not in r.message or "400/min" in r.message for r in caplog.records)
        c.close()


# ---------------------------------------------------------------------------
# log_handler parameter on client
# ---------------------------------------------------------------------------

class TestLogHandlerParam:
    def test_sync_client_callback(self):
        records = []
        handler = CallbackHandler(records.append)
        c = Freshdesk(domain="testdomain", api_key="k", calls_per_minute=0, log_handler=handler)
        assert any(r.getMessage().startswith("Initialized") for r in records)
        logging.getLogger("freshdesk").removeHandler(handler)
        c.close()

    async def test_async_client_callback(self):
        records = []
        handler = CallbackHandler(records.append)
        async with AsyncFreshdesk(
            domain="testdomain", api_key="k", calls_per_minute=0, log_handler=handler
        ) as c:
            assert any(r.getMessage().startswith("Initialized") for r in records)
        logging.getLogger("freshdesk").removeHandler(handler)
