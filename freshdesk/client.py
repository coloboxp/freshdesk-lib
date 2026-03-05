from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Optional, TypeVar, Union
from urllib.parse import urljoin

import httpx

from .exceptions import FreshdeskAPIError, FreshdeskAuthError, FreshdeskRateLimitError
from .rate_limiter import FreshdeskPlan, RateLimiter, resolve_calls_per_minute

from .api.tickets import TicketsAPI, AsyncTicketsAPI
from .api.contacts import ContactsAPI, AsyncContactsAPI
from .api.companies import CompaniesAPI, AsyncCompaniesAPI
from .api.agents import AgentsAPI, AsyncAgentsAPI
from .api.groups import GroupsAPI, AsyncGroupsAPI
from .api.conversations import ConversationsAPI, AsyncConversationsAPI
from .api.roles import RolesAPI, AsyncRolesAPI
from .api.skills import SkillsAPI, AsyncSkillsAPI
from .api.time_entries import TimeEntriesAPI, AsyncTimeEntriesAPI
from .api.custom_objects import CustomObjectsAPI, AsyncCustomObjectsAPI
from .api.canned_responses import CannedResponsesAPI, AsyncCannedResponsesAPI
from .api.discussions import DiscussionsAPI, AsyncDiscussionsAPI
from .api.solutions import SolutionsAPI, AsyncSolutionsAPI
from .api.surveys import SurveysAPI, AsyncSurveysAPI
from .api.minor_resources import MinorResourcesAPI, AsyncMinorResourcesAPI
from .api.automations import AutomationsAPI, AsyncAutomationsAPI
from .api.fields import FieldsAPI, AsyncFieldsAPI
from .api.forms_messages import FormsMessagesAPI, AsyncFormsMessagesAPI
from .api.admin_resources import AdminResourcesAPI, AsyncAdminResourcesAPI
from .api.missing_resources import MissingResourcesAPI, AsyncMissingResourcesAPI

T = TypeVar("T")

log = logging.getLogger("freshdesk.client")


class _BaseClient:
    """Shared initialisation for sync and async clients."""

    def __init__(
        self,
        domain: str,
        api_key: str,
        max_retries: int = 3,
        plan: Union[str, FreshdeskPlan, None] = None,
        calls_per_minute: Optional[int] = None,
        log_handler: Optional[logging.Handler] = None,
    ) -> None:
        self.domain = domain
        self.api_key = api_key
        self.max_retries = max_retries
        self.base_url = f"https://{domain}.freshdesk.com/api/v2/"
        self.auth = (api_key, "X")

        if log_handler is not None:
            logging.getLogger("freshdesk").addHandler(log_handler)

        effective_cpm = resolve_calls_per_minute(plan, calls_per_minute)
        self._rate_limiter: Optional[RateLimiter] = (
            RateLimiter(effective_cpm) if effective_cpm else None
        )

        rl_desc = f"{effective_cpm}/min" if effective_cpm else "disabled"
        log.info(
            "Initialized %s for %s.freshdesk.com (rate_limit=%s, max_retries=%d)",
            type(self).__name__, domain, rl_desc, max_retries,
        )

    @property
    def rate_limiter(self) -> Optional[RateLimiter]:
        return self._rate_limiter

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code in (401, 403):
            log.error("Auth error %d on %s", response.status_code, response.url)
            raise FreshdeskAuthError("Authentication failed or access denied.")

        try:
            error_payload = response.json()
        except Exception:
            error_payload = {"text": response.text}

        log.error(
            "API error %d on %s: %s",
            response.status_code, response.url, error_payload,
        )
        raise FreshdeskAPIError(
            message=f"API Error {response.status_code}",
            status_code=response.status_code,
            error_payload=error_payload,
        )


class Freshdesk(_BaseClient):
    """Synchronous Freshdesk API Client.

    Parameters
    ----------
    domain : str
        Freshdesk subdomain (e.g. ``"mycompany"``).
    api_key : str
        API key for authentication.
    max_retries : int
        How many times to retry on 429 before raising.
    timeout : float
        HTTP request timeout in seconds.
    plan : str | FreshdeskPlan | None
        Freshdesk plan preset (``"growth"``, ``"pro"``, ``"enterprise"``,
        ``"trial"``).  Sets the rate limit automatically.
        Defaults to ``"growth"`` (200 req/min).
    calls_per_minute : int | None
        Custom rate limit override.  Takes priority over *plan*.
        Pass ``0`` to disable the rate limiter entirely.
    log_handler : logging.Handler | None
        Optional handler attached to the ``"freshdesk"`` logger on init.
        Convenience shortcut so callers don't have to touch :mod:`logging`
        directly.  For example, pass a :class:`~freshdesk.log.CallbackHandler`.
    """

    def __init__(
        self,
        domain: str,
        api_key: str,
        max_retries: int = 3,
        timeout: float = 30.0,
        plan: Union[str, FreshdeskPlan, None] = None,
        calls_per_minute: Optional[int] = None,
        log_handler: Optional[logging.Handler] = None,
    ) -> None:
        super().__init__(domain, api_key, max_retries, plan, calls_per_minute, log_handler)
        self.client = httpx.Client(
            base_url=self.base_url,
            auth=self.auth,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )
        self.tickets = TicketsAPI(self)
        self.contacts = ContactsAPI(self)
        self.companies = CompaniesAPI(self)
        self.agents = AgentsAPI(self)
        self.groups = GroupsAPI(self)
        self.conversations = ConversationsAPI(self)
        self.roles = RolesAPI(self)
        self.skills = SkillsAPI(self)
        self.time_entries = TimeEntriesAPI(self)
        self.custom_objects = CustomObjectsAPI(self)
        self.canned_responses = CannedResponsesAPI(self)
        self.discussions = DiscussionsAPI(self)
        self.solutions = SolutionsAPI(self)
        self.surveys = SurveysAPI(self)
        self.minor_resources = MinorResourcesAPI(self)
        self.automations = AutomationsAPI(self)
        self.fields = FieldsAPI(self)
        self.forms_messages = FormsMessagesAPI(self)
        self.admin = AdminResourcesAPI(self)
        self.missing_resources = MissingResourcesAPI(self)

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Make a synchronous HTTP request to the Freshdesk API."""
        if self._rate_limiter is not None:
            self._rate_limiter.acquire()

        url = urljoin(self.base_url, path.lstrip("/"))
        log.debug("→ %s %s", method, path)
        retries = 0

        while retries <= self.max_retries:
            t0 = time.monotonic()
            response = self.client.request(method, url, **kwargs)
            elapsed_ms = (time.monotonic() - t0) * 1000

            if self._rate_limiter is not None:
                self._rate_limiter.update_from_headers(response.headers)

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                if retries >= self.max_retries:
                    log.error(
                        "Rate limit exhausted after %d retries on %s %s",
                        retries, method, path,
                    )
                    raise FreshdeskRateLimitError(
                        "Max retries exceeded for rate limit.", retry_after
                    )
                log.warning(
                    "Rate limited (429) on %s %s – retry %d/%d, waiting %ds",
                    method, path, retries + 1, self.max_retries, retry_after,
                )
                time.sleep(retry_after)
                retries += 1
                continue

            log.debug("← %d %s %s (%.0fms)", response.status_code, method, path, elapsed_ms)

            if not response.is_success:
                self._handle_error(response)

            if response.status_code == 204:
                return None

            if response.headers.get("Content-Type", "").startswith(
                "application/json"
            ):
                return response.json()
            return response.content

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> Freshdesk:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


class AsyncFreshdesk(_BaseClient):
    """Asynchronous Freshdesk API Client.

    Accepts the same parameters as :class:`Freshdesk`.
    """

    def __init__(
        self,
        domain: str,
        api_key: str,
        max_retries: int = 3,
        timeout: float = 30.0,
        plan: Union[str, FreshdeskPlan, None] = None,
        calls_per_minute: Optional[int] = None,
        log_handler: Optional[logging.Handler] = None,
    ) -> None:
        super().__init__(domain, api_key, max_retries, plan, calls_per_minute, log_handler)
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            auth=self.auth,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )
        self.tickets = AsyncTicketsAPI(self)
        self.contacts = AsyncContactsAPI(self)
        self.companies = AsyncCompaniesAPI(self)
        self.agents = AsyncAgentsAPI(self)
        self.groups = AsyncGroupsAPI(self)
        self.conversations = AsyncConversationsAPI(self)
        self.roles = AsyncRolesAPI(self)
        self.skills = AsyncSkillsAPI(self)
        self.time_entries = AsyncTimeEntriesAPI(self)
        self.custom_objects = AsyncCustomObjectsAPI(self)
        self.canned_responses = AsyncCannedResponsesAPI(self)
        self.discussions = AsyncDiscussionsAPI(self)
        self.solutions = AsyncSolutionsAPI(self)
        self.surveys = AsyncSurveysAPI(self)
        self.minor_resources = AsyncMinorResourcesAPI(self)
        self.automations = AsyncAutomationsAPI(self)
        self.fields = AsyncFieldsAPI(self)
        self.forms_messages = AsyncFormsMessagesAPI(self)
        self.admin = AsyncAdminResourcesAPI(self)
        self.missing_resources = AsyncMissingResourcesAPI(self)

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Make an asynchronous HTTP request to the Freshdesk API."""
        if self._rate_limiter is not None:
            await self._rate_limiter.async_acquire()

        url = urljoin(self.base_url, path.lstrip("/"))
        log.debug("→ %s %s", method, path)
        retries = 0

        while retries <= self.max_retries:
            t0 = time.monotonic()
            response = await self.client.request(method, url, **kwargs)
            elapsed_ms = (time.monotonic() - t0) * 1000

            if self._rate_limiter is not None:
                self._rate_limiter.update_from_headers(response.headers)

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                if retries >= self.max_retries:
                    log.error(
                        "Rate limit exhausted after %d retries on %s %s",
                        retries, method, path,
                    )
                    raise FreshdeskRateLimitError(
                        "Max retries exceeded for rate limit.", retry_after
                    )
                log.warning(
                    "Rate limited (429) on %s %s – retry %d/%d, waiting %ds",
                    method, path, retries + 1, self.max_retries, retry_after,
                )
                await asyncio.sleep(retry_after)
                retries += 1
                continue

            log.debug("← %d %s %s (%.0fms)", response.status_code, method, path, elapsed_ms)

            if not response.is_success:
                self._handle_error(response)

            if response.status_code == 204:
                return None

            if response.headers.get("Content-Type", "").startswith(
                "application/json"
            ):
                return response.json()
            return response.content

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> AsyncFreshdesk:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
