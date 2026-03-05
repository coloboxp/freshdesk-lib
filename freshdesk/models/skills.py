from typing import Optional
from datetime import datetime
from .base import FreshdeskModel

class Skill(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
