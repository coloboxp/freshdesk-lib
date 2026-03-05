from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field

from .base import FreshdeskModel

class Contact(FreshdeskModel):
    active: bool = False
    address: Optional[str] = None
    avatar: Optional[Dict[str, Any]] = None
    company_id: Optional[int] = None
    view_all_tickets: Optional[bool] = None
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    deleted: bool = False
    description: Optional[str] = None
    email: Optional[str] = None
    id: int
    job_title: Optional[str] = None
    language: Optional[str] = None
    mobile: Optional[str] = None
    name: str
    other_companies: List[Dict[str, Any]] = Field(default_factory=list)
    other_emails: List[str] = Field(default_factory=list)
    phone: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    time_zone: Optional[str] = None
    twitter_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
