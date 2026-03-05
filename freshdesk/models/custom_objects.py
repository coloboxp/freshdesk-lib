from typing import Dict, Any, List

from .base import FreshdeskModel

class CustomObjectRecord(FreshdeskModel):
    """Pydantic model representing a custom object record. Since these are highly dynamic, we store the dynamic data in a dict, and define the generic schema endpoint base wrapper."""
    id: str
    data: Dict[str, Any]
    
class CustomObjectSchema(FreshdeskModel):
    id: str
    name: str
    description: str
    fields: List[Dict[str, Any]]
