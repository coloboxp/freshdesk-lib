import json
import os
from pathlib import Path

import pytest

from freshdesk import AsyncFreshdesk, Freshdesk
from freshdesk.exceptions import FreshdeskAPIError, FreshdeskAuthError

CONFIG_PATH = Path(__file__).parent / "test_config.json"


def _load_config() -> dict:
    """Load test configuration from file or environment variables.

    Priority: env vars > config file values.
    """
    config: dict = {}
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)

    if os.environ.get("FRESHDESK_DOMAIN"):
        config["domain"] = os.environ["FRESHDESK_DOMAIN"]
    if os.environ.get("FRESHDESK_API_KEY"):
        config["api_key"] = os.environ["FRESHDESK_API_KEY"]

    return config


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def config():
    """Session-scoped Freshdesk credentials (required for integration tests)."""
    cfg = _load_config()
    if not cfg.get("domain") or not cfg.get("api_key"):
        pytest.skip(
            "Freshdesk credentials not configured. "
            "Set FRESHDESK_DOMAIN / FRESHDESK_API_KEY env vars "
            "or create tests/test_config.json"
        )
    return cfg


@pytest.fixture(scope="session")
def client(config):
    """Session-scoped synchronous Freshdesk client."""
    c = Freshdesk(
        domain=config["domain"],
        api_key=config["api_key"],
        max_retries=config.get("max_retries", 1),
        timeout=config.get("timeout", 15.0),
        plan=config.get("plan", "pro"),
    )
    yield c
    c.close()


@pytest.fixture
async def async_client(config):
    """Function-scoped asynchronous Freshdesk client."""
    async with AsyncFreshdesk(
        domain=config["domain"],
        api_key=config["api_key"],
        max_retries=config.get("max_retries", 1),
        timeout=config.get("timeout", 15.0),
        plan=config.get("plan", "pro"),
    ) as c:
        yield c


# ---------------------------------------------------------------------------
# Helpers – call API or skip when feature is unavailable (403/404)
# ---------------------------------------------------------------------------

def api_or_skip(func, *args, **kwargs):
    """Invoke a sync API method; skip the test on 403/404."""
    try:
        return func(*args, **kwargs)
    except FreshdeskAuthError:
        pytest.skip("Feature requires higher plan (403)")
    except FreshdeskAPIError as exc:
        if exc.status_code in (403, 404):
            pytest.skip(f"Feature unavailable (HTTP {exc.status_code})")
        raise


async def async_api_or_skip(coro):
    """Await an async API coroutine; skip the test on 403/404."""
    try:
        return await coro
    except FreshdeskAuthError:
        pytest.skip("Feature requires higher plan (403)")
    except FreshdeskAPIError as exc:
        if exc.status_code in (403, 404):
            pytest.skip(f"Feature unavailable (HTTP {exc.status_code})")
        raise
