from typing import List, Optional, Any
from datetime import datetime

from .base import FreshdeskModel

class Agent(FreshdeskModel):
    available: bool = False
    available_since: Optional[datetime] = None
    contact: Optional[Any] = None # Contact details dictionary
    group_ids: List[int] = []
    id: int
    last_active_at: Optional[datetime] = None
    mobile: Optional[str] = None
    name: Optional[str] = None
    occasional: bool = False
    phone: Optional[str] = None
    role_ids: List[int] = []
    signature: Optional[str] = None
    ticket_scope: int
    created_at: datetime
    updated_at: datetime
