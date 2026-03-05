from __future__ import annotations
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.custom_objects import CustomObjectRecord, CustomObjectSchema

class CustomObjectsAPI:
    """Synchronous implementation of the Custom Objects API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    def create_record(self, schema_id: str, **kwargs: Any) -> CustomObjectRecord:
        """Create a custom object record."""
        res = self._client.request("POST", f"custom_objects/schemas/{schema_id}/records", json=kwargs)
        return CustomObjectRecord.model_validate({"id": res.get("id"), "data": res})

    def retrieve_schemas(self) -> List[CustomObjectSchema]:
        """Retrieve existing custom object schemas."""
        res = self._client.request("GET", "custom_objects/schemas")
        return [CustomObjectSchema.model_validate(s) for s in res.get("schemas", [])]

    def retrieve_schema(self, schema_id: str) -> CustomObjectSchema:
        """Retrieve a specific custom object schema."""
        res = self._client.request("GET", f"custom_objects/schemas/{schema_id}")
        return CustomObjectSchema.model_validate(res)

    def retrieve_record(self, schema_id: str, record_id: str) -> CustomObjectRecord:
        """Retrieve a custom object record by schema and record ID."""
        res = self._client.request("GET", f"custom_objects/schemas/{schema_id}/records/{record_id}")
        return CustomObjectRecord.model_validate({"id": res.get("id"), "data": res})

    def update_record(self, schema_id: str, record_id: str, **kwargs: Any) -> CustomObjectRecord:
        """Update a custom object record."""
        res = self._client.request("PUT", f"custom_objects/schemas/{schema_id}/records/{record_id}", json=kwargs)
        return CustomObjectRecord.model_validate({"id": res.get("id"), "data": res})

    def delete_record(self, schema_id: str, record_id: str) -> None:
        """Delete a custom object record."""
        self._client.request("DELETE", f"custom_objects/schemas/{schema_id}/records/{record_id}")

    def filter_records(self, schema_id: str, **kwargs: Any) -> List[CustomObjectRecord]:
        """Filter records of a custom object."""
        res = self._client.request("GET", f"custom_objects/schemas/{schema_id}/records", params=kwargs)
        records = res.get("records", [])
        return [CustomObjectRecord.model_validate({"id": r.get("id"), "data": r}) for r in records]

class AsyncCustomObjectsAPI:
    """Asynchronous implementation of the Custom Objects API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    async def create_record(self, schema_id: str, **kwargs: Any) -> CustomObjectRecord:
        """Create a custom object record."""
        res = await self._client.request("POST", f"custom_objects/schemas/{schema_id}/records", json=kwargs)
        return CustomObjectRecord.model_validate({"id": res.get("id"), "data": res})

    async def retrieve_schemas(self) -> List[CustomObjectSchema]:
        """Retrieve existing custom object schemas."""
        res = await self._client.request("GET", "custom_objects/schemas")
        return [CustomObjectSchema.model_validate(s) for s in res.get("schemas", [])]

    async def retrieve_schema(self, schema_id: str) -> CustomObjectSchema:
        """Retrieve a specific custom object schema."""
        res = await self._client.request("GET", f"custom_objects/schemas/{schema_id}")
        return CustomObjectSchema.model_validate(res)

    async def retrieve_record(self, schema_id: str, record_id: str) -> CustomObjectRecord:
        """Retrieve a custom object record by schema and record ID."""
        res = await self._client.request("GET", f"custom_objects/schemas/{schema_id}/records/{record_id}")
        return CustomObjectRecord.model_validate({"id": res.get("id"), "data": res})

    async def update_record(self, schema_id: str, record_id: str, **kwargs: Any) -> CustomObjectRecord:
        """Update a custom object record."""
        res = await self._client.request("PUT", f"custom_objects/schemas/{schema_id}/records/{record_id}", json=kwargs)
        return CustomObjectRecord.model_validate({"id": res.get("id"), "data": res})

    async def delete_record(self, schema_id: str, record_id: str) -> None:
        """Delete a custom object record."""
        await self._client.request("DELETE", f"custom_objects/schemas/{schema_id}/records/{record_id}")

    async def filter_records(self, schema_id: str, **kwargs: Any) -> List[CustomObjectRecord]:
        """Filter records of a custom object."""
        res = await self._client.request("GET", f"custom_objects/schemas/{schema_id}/records", params=kwargs)
        records = res.get("records", [])
        return [CustomObjectRecord.model_validate({"id": r.get("id"), "data": r}) for r in records]
