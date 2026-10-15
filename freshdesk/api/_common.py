"""Request-building helpers shared by the API modules."""
from __future__ import annotations

from typing import IO, Any, Dict, Optional, Sequence, Tuple, Union
from urllib.parse import quote, urlencode

#: One file to upload: an open binary file, ``(filename, content)`` or
#: ``(filename, content, content_type)``, where content is bytes or a binary file.
AttachmentInput = Union[
    IO[bytes],
    Tuple[str, Union[bytes, IO[bytes]]],
    Tuple[str, Union[bytes, IO[bytes]], str],
]

MAX_SEARCH_PAGE = 10


def search_path(resource: str, query: str, page: Optional[int] = None) -> str:
    """Build a ``search/<resource>`` path for the filter API.

    Freshdesk requires the query to be wrapped in double quotes and URL
    encoded (spaces as ``%20``), and serves at most 10 pages of 30 results.
    """
    query = query.strip()
    if not (len(query) >= 2 and query.startswith('"') and query.endswith('"')):
        query = f'"{query}"'
    params: Dict[str, Any] = {"query": query}
    if page is not None:
        if not 1 <= page <= MAX_SEARCH_PAGE:
            raise ValueError(f"page must be between 1 and {MAX_SEARCH_PAGE}")
        params["page"] = page
    return f"search/{resource}?{urlencode(params, quote_via=quote)}"


def body_kwargs(
    fields: Dict[str, Any], attachments: Optional[Sequence[AttachmentInput]] = None
) -> Dict[str, Any]:
    """Return httpx request kwargs for a create/update body.

    Without attachments this is a JSON body. With attachments Freshdesk needs
    ``multipart/form-data``: lists become ``key[]`` fields, dicts (for example
    ``custom_fields``) become ``key[sub]`` fields, and each file is sent as
    ``attachments[]``.
    """
    if not attachments:
        return {"json": fields}
    data: Dict[str, Any] = {}
    for key, value in fields.items():
        if isinstance(value, dict):
            for sub, sub_value in value.items():
                data[f"{key}[{sub}]"] = sub_value
        elif isinstance(value, (list, tuple)):
            data[f"{key}[]"] = list(value)
        else:
            data[key] = value
    return {"data": data, "files": [("attachments[]", a) for a in attachments]}
