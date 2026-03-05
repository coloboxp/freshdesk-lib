from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field

from .base import FreshdeskModel

class Company(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    domains: List[str] = Field(default_factory=list)
    note: Optional[str] = None
    health_score: Optional[str] = None
    account_tier: Optional[str] = None
    renewal_date: Optional[datetime] = None
    industry: Optional[str] = None
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
