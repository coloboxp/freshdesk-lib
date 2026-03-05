from typing import Optional, Any, Dict
from datetime import datetime

from .base import FreshdeskModel

class Account(FreshdeskModel):
    id: int
    name: str
    system_name: str
    helpdesk_url: str
    portal_url: str
    primary_contact_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class BusinessHour(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    time_zone: str
    business_hours: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    
class EmailConfig(FreshdeskModel):
    id: int
    name: str
    reply_email: str
    primary: bool = False
    created_at: datetime
    updated_at: datetime

class EmailMailbox(FreshdeskModel):
    id: int
    name: str
    support_email: str
    product_id: Optional[int] = None
    group_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
class Product(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    primary_email: Optional[str] = None
    portal_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
