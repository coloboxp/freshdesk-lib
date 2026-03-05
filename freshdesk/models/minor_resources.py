from typing import List, Optional
from datetime import datetime
from pydantic import Field

from .base import FreshdeskModel

class Job(FreshdeskModel):
    id: str
    status: str
    processed_count: Optional[int] = None
    total_count: Optional[int] = None
    type: str
    created_at: datetime
    updated_at: datetime

class Setting(FreshdeskModel):
    """Helpdesk settings."""
    primary_language: Optional[str] = None
    supported_languages: List[str] = []
    portal_languages: List[str] = []
    portal_url: Optional[str] = None
    helpdesk_url: Optional[str] = None
    name: Optional[str] = None
    language: Optional[str] = None
    time_zone: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
    currency: Optional[str] = None
    custom_mailbox_address: Optional[str] = None


class Thread(FreshdeskModel):
    id: int
    subject: str
    ticket_id: int
    participants: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

class ThreadMessage(FreshdeskModel):
    id: int
    thread_id: int
    body: str
    body_text: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
