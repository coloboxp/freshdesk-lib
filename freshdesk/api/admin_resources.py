from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.admin_resources import Account, BusinessHour, EmailConfig, EmailMailbox, Product

class AdminResourcesAPI:
    """Synchronous implementation of Account, Business Hours, Email Configs/Mailboxes, and Products."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Account
    def view_account_details(self) -> Account:
        """View account details."""
        res = self._client.request("GET", "account")
        return Account.model_validate(res)

    def export_account(self, **kwargs: Any) -> Any:
        """Export account data."""
        return self._client.request("POST", "account/export", json=kwargs)

    # Business Hours
    def list_business_hours(self) -> List[BusinessHour]:
        """List all business hours."""
        res = self._client.request("GET", "business_hours")
        return [BusinessHour.model_validate(b) for b in res]

    def view_business_hour(self, id: int) -> BusinessHour:
        """View a business hour."""
        res = self._client.request("GET", f"business_hours/{id}")
        return BusinessHour.model_validate(res)

    # Email Configs
    def list_email_configs(self) -> List[EmailConfig]:
        """List all email configs."""
        res = self._client.request("GET", "email_configs")
        return [EmailConfig.model_validate(e) for e in res]

    def view_email_config(self, id: int) -> EmailConfig:
        """View an email config."""
        res = self._client.request("GET", f"email_configs/{id}")
        return EmailConfig.model_validate(res)

    # Email Mailboxes
    def create_email_mailbox(self, **kwargs: Any) -> EmailMailbox:
        """Create an email mailbox."""
        res = self._client.request("POST", "email/mailboxes", json=kwargs)
        return EmailMailbox.model_validate(res)

    def list_email_mailboxes(self) -> List[EmailMailbox]:
        """List all email mailboxes."""
        res = self._client.request("GET", "email/mailboxes")
        return [EmailMailbox.model_validate(e) for e in res]

    def view_email_mailbox(self, id: int) -> EmailMailbox:
        """View an email mailbox."""
        res = self._client.request("GET", f"email/mailboxes/{id}")
        return EmailMailbox.model_validate(res)

    def update_email_mailbox(self, id: int, **kwargs: Any) -> EmailMailbox:
        """Update an email mailbox."""
        res = self._client.request("PUT", f"email/mailboxes/{id}", json=kwargs)
        return EmailMailbox.model_validate(res)

    def delete_email_mailbox(self, id: int) -> None:
        """Delete an email mailbox."""
        self._client.request("DELETE", f"email/mailboxes/{id}")
        
    def update_mailbox_settings(self, **kwargs: Any) -> Any:
        """Update mailbox settings."""
        return self._client.request("PUT", "email/settings", json=kwargs)
        
    def view_mailbox_settings(self) -> Any:
        """View mailbox settings."""
        return self._client.request("GET", "email/settings")

    # Products
    def list_products(self) -> List[Product]:
        """List all products."""
        res = self._client.request("GET", "products")
        return [Product.model_validate(p) for p in res]

    def view_product(self, id: int) -> Product:
        """View a product."""
        res = self._client.request("GET", f"products/{id}")
        return Product.model_validate(res)


class AsyncAdminResourcesAPI:
    """Asynchronous implementation of Account, Business Hours, Email Configs/Mailboxes, and Products."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Account
    async def view_account_details(self) -> Account:
        """View account details."""
        res = await self._client.request("GET", "account")
        return Account.model_validate(res)

    async def export_account(self, **kwargs: Any) -> Any:
        """Export account data."""
        return await self._client.request("POST", "account/export", json=kwargs)

    # Business Hours
    async def list_business_hours(self) -> List[BusinessHour]:
        """List all business hours."""
        res = await self._client.request("GET", "business_hours")
        return [BusinessHour.model_validate(b) for b in res]

    async def view_business_hour(self, id: int) -> BusinessHour:
        """View a business hour."""
        res = await self._client.request("GET", f"business_hours/{id}")
        return BusinessHour.model_validate(res)

    # Email Configs
    async def list_email_configs(self) -> List[EmailConfig]:
        """List all email configs."""
        res = await self._client.request("GET", "email_configs")
        return [EmailConfig.model_validate(e) for e in res]

    async def view_email_config(self, id: int) -> EmailConfig:
        """View an email config."""
        res = await self._client.request("GET", f"email_configs/{id}")
        return EmailConfig.model_validate(res)

    # Email Mailboxes
    async def create_email_mailbox(self, **kwargs: Any) -> EmailMailbox:
        """Create an email mailbox."""
        res = await self._client.request("POST", "email/mailboxes", json=kwargs)
        return EmailMailbox.model_validate(res)

    async def list_email_mailboxes(self) -> List[EmailMailbox]:
        """List all email mailboxes."""
        res = await self._client.request("GET", "email/mailboxes")
        return [EmailMailbox.model_validate(e) for e in res]

    async def view_email_mailbox(self, id: int) -> EmailMailbox:
        """View an email mailbox."""
        res = await self._client.request("GET", f"email/mailboxes/{id}")
        return EmailMailbox.model_validate(res)

    async def update_email_mailbox(self, id: int, **kwargs: Any) -> EmailMailbox:
        """Update an email mailbox."""
        res = await self._client.request("PUT", f"email/mailboxes/{id}", json=kwargs)
        return EmailMailbox.model_validate(res)

    async def delete_email_mailbox(self, id: int) -> None:
        """Delete an email mailbox."""
        await self._client.request("DELETE", f"email/mailboxes/{id}")

    async def update_mailbox_settings(self, **kwargs: Any) -> Any:
        """Update mailbox settings."""
        return await self._client.request("PUT", "email/settings", json=kwargs)
        
    async def view_mailbox_settings(self) -> Any:
        """View mailbox settings."""
        return await self._client.request("GET", "email/settings")

    # Products
    async def list_products(self) -> List[Product]:
        """List all products."""
        res = await self._client.request("GET", "products")
        return [Product.model_validate(p) for p in res]

    async def view_product(self, id: int) -> Product:
        """View a product."""
        res = await self._client.request("GET", f"products/{id}")
        return Product.model_validate(res)
