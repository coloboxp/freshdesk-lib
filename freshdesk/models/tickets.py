from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field

from .base import FreshdeskModel

class Ticket(FreshdeskModel):
    id: int
    attachments: List[Dict[str, Any]] = Field(default_factory=list)
    cc_emails: List[str] = Field(default_factory=list)
    company_id: Optional[int] = None
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    deleted: bool = False
    description: Optional[str] = None
    description_text: Optional[str] = None
    due_by: Optional[datetime] = None
    email: Optional[str] = None
    email_config_id: Optional[int] = None
    facebook_id: Optional[str] = None
    fr_due_by: Optional[datetime] = None
    fr_escalated: bool = False
    fwd_emails: List[str] = Field(default_factory=list)
    group_id: Optional[int] = None
    is_escalated: bool = False
    name: Optional[str] = None
    phone: Optional[str] = None
    priority: int
    product_id: Optional[int] = None
    reply_cc_emails: List[str] = Field(default_factory=list)
    requester_id: int
    responder_id: Optional[int] = None
    source: int
    spam: bool = False
    status: int
    subject: str
    tags: List[str] = Field(default_factory=list)
    to_emails: Optional[List[str]] = None
    twitter_id: Optional[str] = None
    type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
