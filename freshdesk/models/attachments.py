from datetime import datetime
from typing import Optional

from pydantic import AliasChoices, Field

from .base import FreshdeskModel


class Attachment(FreshdeskModel):
    """A file attached to a ticket, conversation or canned response.

    Freshdesk returns the byte size as ``size`` on some endpoints and as
    ``file_size`` on others; both are read into :attr:`size`.
    """
    id: int
    name: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = Field(
        default=None, validation_alias=AliasChoices("size", "file_size")
    )
    attachment_url: Optional[str] = None
    thumb_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
