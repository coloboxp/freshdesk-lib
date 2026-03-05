from typing import Optional
from datetime import datetime
from .base import FreshdeskModel

class Role(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    default: bool = False
    created_at: datetime
    updated_at: datetime
