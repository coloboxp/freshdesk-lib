from typing import Any, Dict, Optional, Union
from datetime import datetime

from .base import FreshdeskModel


class SatisfactionRating(FreshdeskModel):
    """Customer satisfaction rating."""
    # Freshdesk returns numbers for some ratings and text such as "_1-72" for others.
    id: Union[int, str]
    survey_id: Optional[int] = None
    user_id: Optional[int] = None
    agent_id: Optional[int] = None
    group_id: Optional[int] = None
    ticket_id: Optional[int] = None
    feedback: Optional[str] = None
    ratings: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Survey(FreshdeskModel):
    id: int
    title: str
    active: bool = False
    created_at: datetime
    updated_at: datetime
