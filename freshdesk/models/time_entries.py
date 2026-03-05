from typing import Optional, Dict, Any
from datetime import datetime

from .base import FreshdeskModel

class TimeEntry(FreshdeskModel):
    id: int
    agent_id: Optional[int] = None
    billable: bool = False
    company_id: Optional[int] = None
    custom_fields: Dict[str, Any] = {}
    executed_at: datetime
    note: Optional[str] = None
    start_time: datetime
    time_spent: str
    timer_running: bool = False
    ticket_id: int
    created_at: datetime
    updated_at: datetime
