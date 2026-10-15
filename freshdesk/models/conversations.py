from typing import List, Optional
from datetime import datetime
from pydantic import Field

from .attachments import Attachment
from .base import FreshdeskModel

class Conversation(FreshdeskModel):
    id: int
    body: Optional[str] = None
    body_text: Optional[str] = None
    attachments: List[Attachment] = Field(default_factory=list)
    incoming: bool = False
    private: bool = False
    source: int
    support_email: Optional[str] = None
    ticket_id: int
    to_emails: Optional[List[str]] = Field(default_factory=list)
    cc_emails: Optional[List[str]] = Field(default_factory=list)
    bcc_emails: Optional[List[str]] = Field(default_factory=list)
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
