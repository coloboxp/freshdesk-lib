# Freshdesk Python Library

A modern, comprehensive, and fully typed Python library for the Freshdesk API (v2).

## Features

- **Fully Typed:** Built entirely on Pydantic v2 models, providing complete IDE autocomplete, type hints, and payload validation.
- **Sync & Async Support:** Offers both synchronous (`Freshdesk`) and asynchronous (`AsyncFreshdesk`) clients using `httpx`.
- **Complete API Coverage:** Comprehensive mapping of all Freshdesk API resources (Tickets, Contacts, Companies, Agents, Groups, Settings, Automations, etc.).
- **Proactive Rate Limiting:** Client-side sliding-window limiter prevents exceeding Freshdesk's per-minute quota. Configurable per plan with self-correction from server headers.
- **Structured Logging:** Built on Python's `logging` module with verbosity levels. One-liner stdout setup or custom callback handler for any destination.
- **Robust Error Handling:** Custom exceptions map directly to specific API failures (Auth, Rate Limits, Validation errors).

## Installation

Requires Python 3.9+.

```bash
pip install .

# With dev/test dependencies
pip install ".[dev]"
```

## Quick Start

### Synchronous Client

```python
from freshdesk import Freshdesk

client = Freshdesk(domain="yourcompany", api_key="your-api-key", plan="pro")

tickets = client.tickets.list(per_page=10)
for ticket in tickets:
    print(f"Ticket #{ticket.id}: {ticket.subject}")

client.close()
```

### Asynchronous Client

```python
import asyncio
from freshdesk import AsyncFreshdesk

async def main():
    async with AsyncFreshdesk(domain="yourcompany", api_key="your-api-key", plan="pro") as client:
        contacts = await client.contacts.list(per_page=5)
        for contact in contacts:
            print(f"Contact: {contact.name}")

asyncio.run(main())
```

### Context Manager (sync)

```python
from freshdesk import Freshdesk

with Freshdesk(domain="yourcompany", api_key="key", plan="pro") as client:
    me = client.agents.me()
    print(f"Logged in as agent #{me.id}")
```

## Rate Limiting

The library enforces Freshdesk's API rate limits **proactively** — it tracks calls in a sliding 60-second window and throttles before exceeding the quota, so you never accidentally burn your limit.

```python
from freshdesk import Freshdesk, FreshdeskPlan

# Plan presets (sets calls/min automatically)
client = Freshdesk(domain="x", api_key="k")                          # Growth (200/min, default)
client = Freshdesk(domain="x", api_key="k", plan="pro")              # Pro (400/min)
client = Freshdesk(domain="x", api_key="k", plan=FreshdeskPlan.ENTERPRISE)  # Enterprise (700/min)

# Custom limit (e.g. purchased additional quota)
client = Freshdesk(domain="x", api_key="k", calls_per_minute=1000)

# Disable rate limiting entirely
client = Freshdesk(domain="x", api_key="k", calls_per_minute=0)
```

| Plan | Rate Limit |
|------|-----------|
| Trial | 50/min |
| Growth | 200/min |
| Pro | 400/min |
| Enterprise | 700/min |

The limiter also reads `X-RateLimit-Remaining` from every response to self-correct when other clients or apps share the same account quota.

## Logging

The library logs under the `"freshdesk"` logger using Python's standard `logging` module. Silent by default.

### Option 1 — stdout (one-liner)

```python
from freshdesk import enable_logging

enable_logging("debug")   # or "info", "warning", "error"
```

### Option 2 — callback handler

```python
from freshdesk import Freshdesk, CallbackHandler

def my_sink(record):
    send_to_my_system(level=record.levelname, msg=record.getMessage())

client = Freshdesk(
    domain="x", api_key="k",
    log_handler=CallbackHandler(my_sink),
)
```

### Option 3 — standard logging (full control)

```python
import logging
logging.getLogger("freshdesk").setLevel(logging.DEBUG)
logging.getLogger("freshdesk").addHandler(my_handler)
```

### Log levels

| Level | What gets logged |
|-------|-----------------|
| DEBUG | Every request/response with method, path, status code, latency (ms). Rate limiter window usage. |
| INFO | Client initialization (domain, plan, rate limit). Rate limiter throttling with wait duration. |
| WARNING | 429 rate limit hits with retry details. Server-side quota corrections. |
| ERROR | Auth failures (401/403). API errors with status and payload. Retries exhausted. |

## Available Resources

All resources follow the `client.<resource>.<action>()` pattern:

- `tickets` — CRUD, filter, restore, forward
- `contacts` — CRUD, filter, search, merge, make_agent, send_invite
- `companies` — CRUD, filter, search
- `agents` — CRUD, me, search
- `groups` — CRUD
- `conversations` — reply, note, update, delete, reply_to_forward
- `roles` — view, list
- `skills` — CRUD
- `time_entries` — CRUD, toggle_timer
- `canned_responses` — CRUD for responses and folders
- `custom_objects` — schemas, records CRUD, filter
- `discussions` — categories, forums, topics, comments (full CRUD)
- `solutions` — categories, folders, articles (full CRUD), search
- `surveys` — list surveys, satisfaction ratings
- `automations` — scenario automations, SLA policies, automation rules
- `fields` — ticket, contact, company fields
- `forms_messages` — ticket forms, outbound messages
- `admin` — account, business hours, email configs/mailboxes, products
- `minor_resources` — jobs, helpdesk settings, collaboration threads/messages
- `missing_resources` — agent availability, admin groups, omnichannel, FSM

## Error Handling

```python
from freshdesk.exceptions import FreshdeskAPIError, FreshdeskRateLimitError, FreshdeskAuthError

try:
    client.tickets.view(999999)
except FreshdeskAuthError:
    print("Invalid credentials or access denied")
except FreshdeskRateLimitError as e:
    print(f"Rate limited. Retry in {e.retry_after}s")
except FreshdeskAPIError as e:
    print(f"API error {e.status_code}: {e.error_payload}")
```

## Testing

Tests live in `tests/` and use `pytest`. Unit tests (mocked) run without credentials. Integration tests require a real Freshdesk instance.

```bash
# Run all tests
pytest

# Run only unit tests (no credentials needed)
pytest tests/test_client.py tests/test_exceptions.py tests/test_models.py tests/test_rate_limiter.py tests/test_logging.py
```

### Configuration

Set credentials via environment variables:

```bash
export FRESHDESK_DOMAIN=your-subdomain
export FRESHDESK_API_KEY=your-api-key
```

Or create `tests/test_config.json` (gitignored):

```json
{
    "domain": "your-subdomain",
    "api_key": "your-api-key",
    "plan": "pro"
}
```

See `tests/test_config.example.json` for reference.
