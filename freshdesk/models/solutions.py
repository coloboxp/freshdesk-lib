from typing import List, Optional
from datetime import datetime
from pydantic import Field

from .base import FreshdeskModel

class SolutionCategory(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    visible_in_portals: List[int] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    
class SolutionFolder(FreshdeskModel):
    id: int
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    visibility: int
    company_ids: List[int] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

class SolutionArticle(FreshdeskModel):
    id: int
    title: str
    description: str
    description_text: Optional[str] = None
    agent_id: Optional[int] = None
    category_id: Optional[int] = None
    folder_id: Optional[int] = None
    hits: int = 0
    status: int
    seo_data: Optional[dict] = None
    tags: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
