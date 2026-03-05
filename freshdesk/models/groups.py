from typing import Optional
from datetime import datetime

from .base import FreshdeskModel

class Group(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    escalate_to: Optional[int] = None
    unassigned_for: Optional[str] = None
    business_hour_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
