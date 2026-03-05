from typing import Optional
from datetime import datetime

from .base import FreshdeskModel

class Category(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
class Forum(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    category_id: int
    forum_visibility: int
    topics_count: int = 0
    created_at: datetime
    updated_at: datetime

class Topic(FreshdeskModel):
    id: int
    title: str
    message: Optional[str] = None
    message_text: Optional[str] = None
    forum_id: int
    hits: int = 0
    posts_count: int = 0
    locked: bool = False
    pinned: bool = False
    created_at: datetime
    updated_at: datetime

class Comment(FreshdeskModel):
    id: int
    body: str
    body_text: Optional[str] = None
    topic_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
