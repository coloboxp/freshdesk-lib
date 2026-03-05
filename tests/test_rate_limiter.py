"""Unit tests for the proactive rate limiter.

All tests are self-contained (no HTTP calls, no credentials).
"""
import time

import pytest

from freshdesk import Freshdesk, AsyncFreshdesk, FreshdeskPlan, RateLimiter
from freshdesk.rate_limiter import PLAN_LIMITS, resolve_calls_per_minute


# ---------------------------------------------------------------------------
# resolve_calls_per_minute
# ---------------------------------------------------------------------------

class TestResolveCPM:
    def test_defaults_to_growth(self):
        assert resolve_calls_per_minute() == 200

    def test_plan_string(self):
        assert resolve_calls_per_minute(plan="pro") == 400

    def test_plan_enum(self):
        assert resolve_calls_per_minute(plan=FreshdeskPlan.ENTERPRISE) == 700

    def test_plan_case_insensitive(self):
        assert resolve_calls_per_minute(plan="Pro") == 400
        assert resolve_calls_per_minute(plan="TRIAL") == 50

    def test_calls_per_minute_overrides_plan(self):
        assert resolve_calls_per_minute(plan="pro", calls_per_minute=999) == 999

    def test_calls_per_minute_zero_disables(self):
        assert resolve_calls_per_minute(calls_per_minute=0) is None

    def test_calls_per_minute_none_falls_to_plan(self):
        assert resolve_calls_per_minute(plan="enterprise", calls_per_minute=None) == 700

    def test_invalid_plan_raises(self):
        with pytest.raises(ValueError):
            resolve_calls_per_minute(plan="nonexistent")


# ---------------------------------------------------------------------------
# FreshdeskPlan enum
# ---------------------------------------------------------------------------

class TestFreshdeskPlan:
    def test_all_plans_have_limits(self):
        for plan in FreshdeskPlan:
            assert plan in PLAN_LIMITS
            assert PLAN_LIMITS[plan] > 0

    def test_plan_values(self):
        assert FreshdeskPlan.TRIAL.value == "trial"
        assert FreshdeskPlan.GROWTH.value == "growth"
        assert FreshdeskPlan.PRO.value == "pro"
        assert FreshdeskPlan.ENTERPRISE.value == "enterprise"


# ---------------------------------------------------------------------------
# RateLimiter – basic behaviour
# ---------------------------------------------------------------------------

class TestRateLimiter:
    def test_properties(self):
        rl = RateLimiter(calls_per_minute=100)
        assert rl.calls_per_minute == 100
        assert rl.current_usage == 0

    def test_acquire_tracks_usage(self):
        rl = RateLimiter(calls_per_minute=100)
        rl.acquire()
        rl.acquire()
        assert rl.current_usage == 2

    def test_acquire_returns_zero_when_no_wait(self):
        rl = RateLimiter(calls_per_minute=100)
        waited = rl.acquire()
        assert waited == 0.0

    def test_acquire_blocks_at_limit(self):
        rl = RateLimiter(calls_per_minute=3)
        rl.acquire()
        rl.acquire()
        rl.acquire()

        start = time.monotonic()
        rl._timestamps[0] = time.monotonic() - 59.5  # oldest call almost expired
        rl.acquire()
        elapsed = time.monotonic() - start
        assert elapsed < 1.0  # waited ~0.5s for the oldest to expire

    def test_eviction_frees_slots(self):
        rl = RateLimiter(calls_per_minute=5)
        for _ in range(5):
            rl.acquire()
        assert rl.current_usage == 5

        for ts in list(rl._timestamps):
            rl._timestamps.remove(ts)
            rl._timestamps.appendleft(time.monotonic() - 61)
        assert rl.current_usage == 0


# ---------------------------------------------------------------------------
# RateLimiter – async
# ---------------------------------------------------------------------------

class TestRateLimiterAsync:
    async def test_async_acquire(self):
        rl = RateLimiter(calls_per_minute=100)
        waited = await rl.async_acquire()
        assert waited == 0.0
        assert rl.current_usage == 1

    async def test_async_acquire_tracks_usage(self):
        rl = RateLimiter(calls_per_minute=100)
        await rl.async_acquire()
        await rl.async_acquire()
        await rl.async_acquire()
        assert rl.current_usage == 3


# ---------------------------------------------------------------------------
# RateLimiter – header self-correction
# ---------------------------------------------------------------------------

class TestRateLimiterHeaderCorrection:
    def test_update_tightens_when_server_shows_less(self):
        rl = RateLimiter(calls_per_minute=100)
        rl.acquire()
        assert rl.current_usage == 1  # local thinks 99 remaining

        rl.update_from_headers({"X-RateLimit-Remaining": "50"})
        assert rl.current_usage == 50  # 100 - 50 = 50 used

    def test_update_ignores_when_server_shows_more(self):
        rl = RateLimiter(calls_per_minute=100)
        for _ in range(30):
            rl.acquire()
        rl.update_from_headers({"X-RateLimit-Remaining": "90"})
        assert rl.current_usage == 30  # no change, server is more generous

    def test_update_handles_missing_header(self):
        rl = RateLimiter(calls_per_minute=100)
        rl.acquire()
        rl.update_from_headers({})
        assert rl.current_usage == 1

    def test_update_handles_lowercase_header(self):
        rl = RateLimiter(calls_per_minute=100)
        rl.acquire()
        rl.update_from_headers({"x-ratelimit-remaining": "10"})
        assert rl.current_usage == 90

    def test_update_handles_bad_value(self):
        rl = RateLimiter(calls_per_minute=100)
        rl.acquire()
        rl.update_from_headers({"X-RateLimit-Remaining": "not_a_number"})
        assert rl.current_usage == 1  # unchanged


# ---------------------------------------------------------------------------
# Client integration – limiter is wired up
# ---------------------------------------------------------------------------

class TestClientLimiterIntegration:
    def test_sync_client_default_limiter(self):
        c = Freshdesk(domain="test", api_key="k")
        assert c.rate_limiter is not None
        assert c.rate_limiter.calls_per_minute == 200  # Growth default
        c.close()

    def test_sync_client_plan_pro(self):
        c = Freshdesk(domain="test", api_key="k", plan="pro")
        assert c.rate_limiter is not None
        assert c.rate_limiter.calls_per_minute == 400
        c.close()

    def test_sync_client_plan_enum(self):
        c = Freshdesk(domain="test", api_key="k", plan=FreshdeskPlan.ENTERPRISE)
        assert c.rate_limiter is not None
        assert c.rate_limiter.calls_per_minute == 700
        c.close()

    def test_sync_client_custom_cpm(self):
        c = Freshdesk(domain="test", api_key="k", calls_per_minute=999)
        assert c.rate_limiter is not None
        assert c.rate_limiter.calls_per_minute == 999
        c.close()

    def test_sync_client_disabled_limiter(self):
        c = Freshdesk(domain="test", api_key="k", calls_per_minute=0)
        assert c.rate_limiter is None
        c.close()

    async def test_async_client_default_limiter(self):
        async with AsyncFreshdesk(domain="test", api_key="k") as c:
            assert c.rate_limiter is not None
            assert c.rate_limiter.calls_per_minute == 200

    async def test_async_client_plan_pro(self):
        async with AsyncFreshdesk(domain="test", api_key="k", plan="pro") as c:
            assert c.rate_limiter is not None
            assert c.rate_limiter.calls_per_minute == 400

    async def test_async_client_disabled(self):
        async with AsyncFreshdesk(domain="test", api_key="k", calls_per_minute=0) as c:
            assert c.rate_limiter is None
