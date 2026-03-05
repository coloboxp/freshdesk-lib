from typing import Optional
from datetime import datetime

from .base import FreshdeskModel

class ScenarioAutomation(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
class SLAPolicy(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class AutomationRule(FreshdeskModel):
    id: int
    name: str
    position: int
    active: bool
    created_at: datetime
    updated_at: datetime
