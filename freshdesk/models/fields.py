from typing import Optional, Any
from datetime import datetime

from .base import FreshdeskModel

class Field(FreshdeskModel):
    id: int
    name: str
    label: str
    description: Optional[str] = None
    position: int
    type: str
    portal_cc: bool = False
    portal_cc_to: str = "requester"
    choices: Optional[Any] = None
    created_at: datetime
    updated_at: datetime
    
class TicketField(Field):
    pass

class ContactField(Field):
    pass

class CompanyField(Field):
    pass
