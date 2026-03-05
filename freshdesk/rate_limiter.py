"""Proactive client-side rate limiter for the Freshdesk API.

Freshdesk enforces per-minute rate limits that vary by plan.  This module
provides a sliding-window limiter that **prevents** exceeding the quota
instead of just reacting to 429 responses.

It also reads ``X-RateLimit-Remaining`` from every response to self-correct
when other clients or apps share the same account quota.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections import deque
from enum import Enum
from threading import Lock
from typing import Any, Dict, Optional, Union

log = logging.getLogger("freshdesk.rate_limiter")


# ---------------------------------------------------------------------------
# Plan presets
# ---------------------------------------------------------------------------

class FreshdeskPlan(str, Enum):
    """Supported Freshdesk plan tiers (determines API rate limits)."""
    TRIAL = "trial"
    GROWTH = "growth"
    PRO = "pro"
    ENTERPRISE = "enterprise"


PLAN_LIMITS: Dict[FreshdeskPlan, int] = {
    FreshdeskPlan.TRIAL: 50,
    FreshdeskPlan.GROWTH: 200,
    FreshdeskPlan.PRO: 400,
    FreshdeskPlan.ENTERPRISE: 700,
}

DEFAULT_PLAN = FreshdeskPlan.GROWTH


def resolve_calls_per_minute(
    plan: Union[str, FreshdeskPlan, None] = None,
    calls_per_minute: Optional[int] = None,
) -> Optional[int]:
    """Determine the effective calls-per-minute value.

    * *calls_per_minute* takes highest priority (explicit override).
      Pass ``0`` or ``None`` to **disable** the limiter.
    * *plan* selects a preset.  Accepts a :class:`FreshdeskPlan` value or
      a lowercase string (``"pro"``, ``"enterprise"``, …).
    * When neither is given, defaults to **Growth** (200 req/min).

    Returns ``None`` when limiting is disabled, otherwise a positive int.
    """
    if calls_per_minute is not None:
        return calls_per_minute if calls_per_minute > 0 else None

    if plan is not None:
        if isinstance(plan, str):
            plan = FreshdeskPlan(plan.lower())
        return PLAN_LIMITS[plan]

    return PLAN_LIMITS[DEFAULT_PLAN]


# ---------------------------------------------------------------------------
# Sliding-window rate limiter
# ---------------------------------------------------------------------------

class RateLimiter:
    """Thread-safe / async-safe sliding-window rate limiter.

    Tracks request timestamps over a 60-second window and blocks (sync)
    or awaits (async) when the next request would exceed the budget.

    After every HTTP response the caller should invoke
    :meth:`update_from_headers` so the limiter can self-correct against
    the server-reported remaining quota (shared across all API consumers
    on the same Freshdesk account).
    """

    def __init__(self, calls_per_minute: int) -> None:
        self._max_calls = calls_per_minute
        self._window = 60.0
        self._timestamps: deque[float] = deque()
        self._lock = Lock()
        self._async_lock: Optional[asyncio.Lock] = None

    # -- public properties ---------------------------------------------------

    @property
    def calls_per_minute(self) -> int:
        return self._max_calls

    @property
    def current_usage(self) -> int:
        """Number of calls tracked in the current sliding window."""
        now = time.monotonic()
        self._evict(now)
        return len(self._timestamps)

    # -- internal helpers ----------------------------------------------------

    def _evict(self, now: float) -> None:
        cutoff = now - self._window
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

    # -- sync API ------------------------------------------------------------

    def acquire(self) -> float:
        """Block until a request slot is available.

        Returns the number of seconds the caller was forced to wait (0.0
        when no waiting was needed).
        """
        with self._lock:
            waited = 0.0
            now = time.monotonic()
            self._evict(now)

            if len(self._timestamps) >= self._max_calls:
                sleep_for = self._timestamps[0] + self._window - time.monotonic()
                if sleep_for > 0:
                    log.info(
                        "Rate limit reached (%d/%d), throttling for %.1fs",
                        len(self._timestamps), self._max_calls, sleep_for,
                    )
                    time.sleep(sleep_for)
                    waited += sleep_for
                now = time.monotonic()
                self._evict(now)

            self._timestamps.append(time.monotonic())
            log.debug("Rate limiter: %d/%d calls in window", len(self._timestamps), self._max_calls)
            return waited

    # -- async API -----------------------------------------------------------

    async def async_acquire(self) -> float:
        """Async equivalent of :meth:`acquire`."""
        if self._async_lock is None:
            self._async_lock = asyncio.Lock()

        async with self._async_lock:
            waited = 0.0
            now = time.monotonic()
            self._evict(now)

            if len(self._timestamps) >= self._max_calls:
                sleep_for = self._timestamps[0] + self._window - time.monotonic()
                if sleep_for > 0:
                    log.info(
                        "Rate limit reached (%d/%d), throttling for %.1fs",
                        len(self._timestamps), self._max_calls, sleep_for,
                    )
                    await asyncio.sleep(sleep_for)
                    waited += sleep_for
                now = time.monotonic()
                self._evict(now)

            self._timestamps.append(time.monotonic())
            log.debug("Rate limiter: %d/%d calls in window", len(self._timestamps), self._max_calls)
            return waited

    # -- header self-correction ----------------------------------------------

    def update_from_headers(self, headers: Any) -> None:
        """Read ``X-RateLimit-Remaining`` and adjust local state.

        If the server reports fewer remaining calls than the local window
        predicts, synthetic timestamps are injected to tighten the window
        so the limiter slows down proactively.
        """
        raw = (
            headers.get("X-RateLimit-Remaining")
            or headers.get("x-ratelimit-remaining")
        )
        if raw is None:
            return
        try:
            server_remaining = int(raw)
        except (ValueError, TypeError):
            return

        with self._lock:
            now = time.monotonic()
            self._evict(now)

            local_used = len(self._timestamps)
            local_remaining = self._max_calls - local_used

            log.debug("Server reports %d remaining (local estimate: %d)", server_remaining, local_remaining)

            if server_remaining < local_remaining:
                deficit = local_remaining - server_remaining
                log.warning(
                    "Rate limit correction: server says %d remaining vs local %d – "
                    "tightening by %d (other clients may share quota)",
                    server_remaining, local_remaining, deficit,
                )
                for _ in range(deficit):
                    self._timestamps.append(now)
