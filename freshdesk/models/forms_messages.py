from typing import Optional
from datetime import datetime

from .base import FreshdeskModel

class TicketForm(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class OutboundMessage(FreshdeskModel):
    id: int
    body: str
    channel_id: int
    recipient_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
