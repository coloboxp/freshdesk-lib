from typing import Any, TypeVar, Generic, List, Optional, get_args
from pydantic import BaseModel, ConfigDict, model_validator

T = TypeVar('T')

class FreshdeskModel(BaseModel):
    """Base Pydantic model for all Freshdesk models."""
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
        from_attributes=True,
    )

    @model_validator(mode="before")
    @classmethod
    def _null_lists_to_empty(cls, data: Any) -> Any:
        """Freshdesk sends null for empty lists on some records (e.g. reply_cc_emails on older
        tickets). Treat null as an empty list for every non-nullable list field that defaults to one;
        fields typed Optional keep None."""
        if not isinstance(data, dict):
            return data
        empty = [name for name, field in cls.model_fields.items()
                 if data.get(field.alias or name, 0) is None and field.default_factory is list
                 and type(None) not in get_args(field.annotation)]
        return {**data, **{cls.model_fields[name].alias or name: [] for name in empty}} if empty else data

class PaginatedList(BaseModel, Generic[T]):
    """Represents a paginated list of resources."""
    items: List[T]
    total: Optional[int] = None
    next_page: Optional[str] = None
