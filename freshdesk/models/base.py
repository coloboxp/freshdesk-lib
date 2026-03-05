from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')

class FreshdeskModel(BaseModel):
    """Base Pydantic model for all Freshdesk models."""
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
        from_attributes=True,
    )

class PaginatedList(BaseModel, Generic[T]):
    """Represents a paginated list of resources."""
    items: List[T]
    total: Optional[int] = None
    next_page: Optional[str] = None
