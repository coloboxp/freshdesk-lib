from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import Field

from .base import FreshdeskModel

class Company(FreshdeskModel):
    id: int
    name: str
    org_company_id: Optional[Union[int, str]] = None
    description: Optional[str] = None
    domains: List[str] = Field(default_factory=list)
    note: Optional[str] = None
    health_score: Optional[str] = None
    account_tier: Optional[str] = None
    renewal_date: Optional[datetime] = None
    industry: Optional[str] = None
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
