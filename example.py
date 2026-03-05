import os
import asyncio
from freshdesk import Freshdesk, AsyncFreshdesk
from freshdesk.exceptions import FreshdeskAPIError

# To run this script, set your Freshdesk domain and API key as environment variables:
# export FRESHDESK_DOMAIN="yourdomain"
# export FRESHDESK_API_KEY="your_api_key"

def run_sync_example():
    print("--- Running Synchronous Example ---")
    domain = os.getenv("FRESHDESK_DOMAIN")
    api_key = os.getenv("FRESHDESK_API_KEY")

    if not domain or not api_key:
        print("Please set FRESHDESK_DOMAIN and FRESHDESK_API_KEY environment variables.")
        return

    # Using context manager for automatic cleanup
    with Freshdesk(domain=domain, api_key=api_key) as client:
        try:
            # 1. Fetch the first page of tickets
            print("Fetching recent tickets...")
            tickets = client.tickets.list(per_page=3)
            for t in tickets:
                print(f"  [{t.id}] {t.subject} (Status: {t.status})")

            # 2. Fetch the current account details
            print("\nFetching account details...")
            account = client.admin.view_account_details()
            print(f"  Account Name: {account.name}")
            print(f"  Helpdesk URL: {account.helpdesk_url}")
            
            # 3. List agents
            print("\nFetching agents...")
            agents = client.agents.list(per_page=3)
            for a in agents:
                print(f"  [{a.id}] {a.contact.name if a.contact else 'Unknown'} - {a.contact.email if a.contact else ''}")

        except FreshdeskAPIError as e:
            print(f"API Error occurred: HTTP {e.status_code}")
            print(e.error_payload)


async def run_async_example():
    print("\n--- Running Asynchronous Example ---")
    domain = os.getenv("FRESHDESK_DOMAIN")
    api_key = os.getenv("FRESHDESK_API_KEY")

    if not domain or not api_key:
        print("Please set FRESHDESK_DOMAIN and FRESHDESK_API_KEY environment variables.")
        return

    async with AsyncFreshdesk(domain=domain, api_key=api_key) as client:
        try:
            # We can fetch multiple resources concurrently!
            print("Fetching tickets, contacts, and companies concurrently...")
            
            tickets_task = client.tickets.list(per_page=3)
            contacts_task = client.contacts.list(per_page=3)
            companies_task = client.companies.list(per_page=3)
            
            # Await all at once
            tickets, contacts, companies = await asyncio.gather(
                tickets_task, contacts_task, companies_task
            )
            
            print(f"Loaded {len(tickets)} tickets, {len(contacts)} contacts, and {len(companies)} companies.")
            
            print("\nTop Contacts:")
            for c in contacts:
                print(f"  - {c.name} ({c.email})")

        except FreshdeskAPIError as e:
            print(f"API Error occurred: HTTP {e.status_code}")
            print(e.error_payload)

if __name__ == "__main__":
    run_sync_example()
    asyncio.run(run_async_example())
