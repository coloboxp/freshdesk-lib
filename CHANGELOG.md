# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- **Structured logging** (`freshdesk/log.py`):
  - Uses Python's standard `logging` module under the `"freshdesk"` logger hierarchy.
  - **DEBUG**: every request/response with method, path, status, and latency in ms.
  - **INFO**: client initialization (domain, plan, rate limit), rate limiter throttling.
  - **WARNING**: 429 rate limit hits with retry info, server-side quota corrections.
  - **ERROR**: auth failures, API errors with payload, retries exhausted.
  - `enable_logging("debug")` — one-liner to turn on stdout logging at any level.
  - `CallbackHandler(my_fn)` — routes log records to a user-supplied callback.
  - `log_handler=` parameter on `Freshdesk` / `AsyncFreshdesk` to attach a handler at init.
- **Proactive rate limiter** (`freshdesk/rate_limiter.py`):
  - Sliding-window limiter that **prevents** exceeding Freshdesk's per-minute API quota (instead of just reacting to 429 errors).
  - Plan presets via `FreshdeskPlan` enum: `trial` (50/min), `growth` (200/min), `pro` (400/min), `enterprise` (700/min).
  - Defaults to **Growth** (200 req/min) — safe conservative default.
  - Configurable: `Freshdesk(domain, api_key, plan="pro")` or `Freshdesk(domain, api_key, calls_per_minute=500)`.
  - Pass `calls_per_minute=0` to disable the limiter entirely.
  - Self-corrects from `X-RateLimit-Remaining` response headers so the limiter adapts when other clients share the same account quota.
  - Thread-safe for sync clients, async-safe for async clients.

### Fixed

- **ScenarioAutomation model** (`freshdesk/models/automations.py`):
  - Made `created_at` and `updated_at` fields optional since the API may not return them.
- **Integration tests** (`tests/test_api_*.py`):
  - All create operations now use a per-run UUID suffix (`_RUN_ID`) for emails, names, and titles to avoid 409 Conflict errors from leftover data across test runs.
- **Integration test helpers** (`tests/conftest.py`):
  - `api_or_skip` and `async_api_or_skip` now catch `FreshdeskAuthError` (403 for enterprise-only features) in addition to `FreshdeskAPIError` with status 403/404.
- **Admin API tests** (`tests/test_api_admin.py`):
  - Thread creation uses correct payload: `type`, `title`, and `parent` (with `parent_id` and `type`) instead of `subject` and `ticket_id`.
  - `test_view_account` and `test_export_account` (sync and async) use `api_or_skip` / `async_api_or_skip` for enterprise-only features.
- **Core API tests** (`tests/test_api_core.py`):
  - Ticket creation wrapped in try/except to skip with descriptive message when instance has mandatory custom fields (400).
  - Contact and company creation wrapped in try/except to skip gracefully on 400 (mandatory custom fields or validation rules).
- **Support API tests** (`tests/test_api_support.py`):
  - Ticket creation (TimeEntries) and folder creation (CannedResponses) wrapped in try/except to skip on 400.
- **Content API tests** (`tests/test_api_content.py`):
  - Discussion category creation wrapped in try/except to skip on 400.
- **Admin API tests** (`tests/test_api_admin.py`):
  - Ticket creation in `test_thread_lifecycle` wrapped in try/except to skip on 400.

- **Pydantic models aligned with real Freshdesk API**:
  - `Setting` (`minor_resources.py`): All fields optional; added `primary_language`, `supported_languages`, `portal_languages`; removed required fields that don't exist in GET /api/v2/settings/helpdesk response.
  - `SatisfactionRating` (`surveys.py`): Replaced `customer_id`/`rating` with `user_id`/`ratings` dict; all fields except `id` optional to match satisfaction ratings API response.

- **Circular imports in all 20 API modules**: Replaced direct `from ..client import Freshdesk, AsyncFreshdesk` with `TYPE_CHECKING`-guarded imports to resolve circular import at runtime.

- **Comprehensive test suite** targeting 90%+ coverage with real Freshdesk API integration tests:
  - `tests/conftest.py` – config loading (env vars or `test_config.json`), session-scoped sync client, function-scoped async client, `api_or_skip` / `async_api_or_skip` helpers.
  - `tests/test_client.py` – 21 mocked unit tests covering all client code paths (success, 204, non-JSON, auth errors, rate limit, API errors, context managers) plus 5 real integration tests.
  - `tests/test_exceptions.py` – exception hierarchy and attribute tests.
  - `tests/test_models.py` – validation tests for all 30+ Pydantic models (100% model coverage).
  - `tests/test_api_core.py` – sync + async integration tests for tickets, contacts, companies, agents, groups, conversations.
  - `tests/test_api_support.py` – sync + async integration tests for roles, skills, time entries, canned responses, custom objects.
  - `tests/test_api_content.py` – sync + async integration tests for discussions, solutions, surveys.
  - `tests/test_api_admin.py` – sync + async integration tests for automations, fields, forms/messages, admin resources, minor resources, missing resources.
  - `tests/test_config.example.json` – example credentials file.
- **Coverage configuration** in `pyproject.toml`: branch coverage, HTML report, 90% fail-under threshold.
- **Hatch build config** added `[tool.hatch.build.targets.wheel]` with `packages = ["freshdesk"]`.
- **Pydantic models aligned with Freshdesk API responses**:
  - `tickets.py`: `to_emails` → `Optional[List[str]]` (API returns `null`).
  - `fields.py`: `choices` → `Optional[Any]` (can be dict or list depending on field type).
  - `admin_resources.py`: `BusinessHour.business_hours` → `Dict[str, Any]` (keyed by day name, not a list).
  - `solutions.py`: `SolutionFolder.category_id` → `Optional[int]` (not always returned).
  - `canned_responses.py`: `CannedResponseFolder.created_at` and `updated_at` → `Optional[datetime]` (create response omits them).
