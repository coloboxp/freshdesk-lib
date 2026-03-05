from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.discussions import Category, Forum, Topic, Comment

class DiscussionsAPI:
    """Synchronous implementation of the Discussions API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Forum categories
    def list_categories(self, **kwargs: Any) -> List[Category]:
        res = self._client.request("GET", "discussions/categories", params=kwargs)
        return [Category.model_validate(c) for c in res]

    def view_category(self, id: int) -> Category:
        res = self._client.request("GET", f"discussions/categories/{id}")
        return Category.model_validate(res)

    def create_category(self, **kwargs: Any) -> Category:
        res = self._client.request("POST", "discussions/categories", json=kwargs)
        return Category.model_validate(res)

    def update_category(self, id: int, **kwargs: Any) -> Category:
        res = self._client.request("PUT", f"discussions/categories/{id}", json=kwargs)
        return Category.model_validate(res)

    def delete_category(self, id: int) -> None:
        self._client.request("DELETE", f"discussions/categories/{id}")

    # Forums
    def list_forums(self, category_id: int, **kwargs: Any) -> List[Forum]:
        res = self._client.request("GET", f"discussions/categories/{category_id}/forums", params=kwargs)
        return [Forum.model_validate(f) for f in res]

    def view_forum(self, id: int) -> Forum:
        res = self._client.request("GET", f"discussions/forums/{id}")
        return Forum.model_validate(res)

    def create_forum(self, category_id: int, **kwargs: Any) -> Forum:
        res = self._client.request("POST", f"discussions/categories/{category_id}/forums", json=kwargs)
        return Forum.model_validate(res)

    def update_forum(self, id: int, **kwargs: Any) -> Forum:
        res = self._client.request("PUT", f"discussions/forums/{id}", json=kwargs)
        return Forum.model_validate(res)

    def delete_forum(self, id: int) -> None:
        self._client.request("DELETE", f"discussions/forums/{id}")

    # Topics
    def list_topics(self, forum_id: int, **kwargs: Any) -> List[Topic]:
        res = self._client.request("GET", f"discussions/forums/{forum_id}/topics", params=kwargs)
        return [Topic.model_validate(t) for t in res]

    def list_all_topics(self, **kwargs: Any) -> List[Topic]:
        res = self._client.request("GET", "discussions/topics", params=kwargs)
        return [Topic.model_validate(t) for t in res]

    def view_topic(self, id: int) -> Topic:
        res = self._client.request("GET", f"discussions/topics/{id}")
        return Topic.model_validate(res)

    def create_topic(self, forum_id: int, **kwargs: Any) -> Topic:
        res = self._client.request("POST", f"discussions/forums/{forum_id}/topics", json=kwargs)
        return Topic.model_validate(res)

    def update_topic(self, id: int, **kwargs: Any) -> Topic:
        res = self._client.request("PUT", f"discussions/topics/{id}", json=kwargs)
        return Topic.model_validate(res)

    def delete_topic(self, id: int) -> None:
        self._client.request("DELETE", f"discussions/topics/{id}")

    # Comments
    def list_comments(self, topic_id: int, **kwargs: Any) -> List[Comment]:
        res = self._client.request("GET", f"discussions/topics/{topic_id}/comments", params=kwargs)
        return [Comment.model_validate(c) for c in res]

    def create_comment(self, topic_id: int, **kwargs: Any) -> Comment:
        res = self._client.request("POST", f"discussions/topics/{topic_id}/comments", json=kwargs)
        return Comment.model_validate(res)

    def update_comment(self, topic_id: int, id: int, **kwargs: Any) -> Comment:
        res = self._client.request("PUT", f"discussions/topics/{topic_id}/comments/{id}", json=kwargs)
        return Comment.model_validate(res)

    def delete_comment(self, topic_id: int, id: int) -> None:
        self._client.request("DELETE", f"discussions/topics/{topic_id}/comments/{id}")


class AsyncDiscussionsAPI:
    """Asynchronous implementation of the Discussions API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Forum categories
    async def list_categories(self, **kwargs: Any) -> List[Category]:
        res = await self._client.request("GET", "discussions/categories", params=kwargs)
        return [Category.model_validate(c) for c in res]

    async def view_category(self, id: int) -> Category:
        res = await self._client.request("GET", f"discussions/categories/{id}")
        return Category.model_validate(res)

    async def create_category(self, **kwargs: Any) -> Category:
        res = await self._client.request("POST", "discussions/categories", json=kwargs)
        return Category.model_validate(res)

    async def update_category(self, id: int, **kwargs: Any) -> Category:
        res = await self._client.request("PUT", f"discussions/categories/{id}", json=kwargs)
        return Category.model_validate(res)

    async def delete_category(self, id: int) -> None:
        await self._client.request("DELETE", f"discussions/categories/{id}")

    # Forums
    async def list_forums(self, category_id: int, **kwargs: Any) -> List[Forum]:
        res = await self._client.request("GET", f"discussions/categories/{category_id}/forums", params=kwargs)
        return [Forum.model_validate(f) for f in res]

    async def view_forum(self, id: int) -> Forum:
        res = await self._client.request("GET", f"discussions/forums/{id}")
        return Forum.model_validate(res)

    async def create_forum(self, category_id: int, **kwargs: Any) -> Forum:
        res = await self._client.request("POST", f"discussions/categories/{category_id}/forums", json=kwargs)
        return Forum.model_validate(res)

    async def update_forum(self, id: int, **kwargs: Any) -> Forum:
        res = await self._client.request("PUT", f"discussions/forums/{id}", json=kwargs)
        return Forum.model_validate(res)

    async def delete_forum(self, id: int) -> None:
        await self._client.request("DELETE", f"discussions/forums/{id}")

    # Topics
    async def list_topics(self, forum_id: int, **kwargs: Any) -> List[Topic]:
        res = await self._client.request("GET", f"discussions/forums/{forum_id}/topics", params=kwargs)
        return [Topic.model_validate(t) for t in res]

    async def list_all_topics(self, **kwargs: Any) -> List[Topic]:
        res = await self._client.request("GET", "discussions/topics", params=kwargs)
        return [Topic.model_validate(t) for t in res]

    async def view_topic(self, id: int) -> Topic:
        res = await self._client.request("GET", f"discussions/topics/{id}")
        return Topic.model_validate(res)

    async def create_topic(self, forum_id: int, **kwargs: Any) -> Topic:
        res = await self._client.request("POST", f"discussions/forums/{forum_id}/topics", json=kwargs)
        return Topic.model_validate(res)

    async def update_topic(self, id: int, **kwargs: Any) -> Topic:
        res = await self._client.request("PUT", f"discussions/topics/{id}", json=kwargs)
        return Topic.model_validate(res)

    async def delete_topic(self, id: int) -> None:
        await self._client.request("DELETE", f"discussions/topics/{id}")

    # Comments
    async def list_comments(self, topic_id: int, **kwargs: Any) -> List[Comment]:
        res = await self._client.request("GET", f"discussions/topics/{topic_id}/comments", params=kwargs)
        return [Comment.model_validate(c) for c in res]

    async def create_comment(self, topic_id: int, **kwargs: Any) -> Comment:
        res = await self._client.request("POST", f"discussions/topics/{topic_id}/comments", json=kwargs)
        return Comment.model_validate(res)

    async def update_comment(self, topic_id: int, id: int, **kwargs: Any) -> Comment:
        res = await self._client.request("PUT", f"discussions/topics/{topic_id}/comments/{id}", json=kwargs)
        return Comment.model_validate(res)

    async def delete_comment(self, topic_id: int, id: int) -> None:
        await self._client.request("DELETE", f"discussions/topics/{topic_id}/comments/{id}")
