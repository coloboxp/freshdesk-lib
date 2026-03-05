from typing import Optional
from datetime import datetime

from .base import FreshdeskModel

class CannedResponseFolder(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    responses_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CannedResponse(FreshdeskModel):
    id: int
    content: str
    content_html: str
    folder_id: Optional[int] = None
    title: str
    created_at: datetime
    updated_at: datetime
