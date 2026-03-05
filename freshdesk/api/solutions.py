from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..client import Freshdesk, AsyncFreshdesk
from ..models.solutions import SolutionCategory, SolutionFolder, SolutionArticle

class SolutionsAPI:
    """Synchronous implementation of the Solutions API."""
    def __init__(self, client: Freshdesk):
        self._client = client

    # Categories
    def list_categories(self, **kwargs: Any) -> List[SolutionCategory]:
        res = self._client.request("GET", "solutions/categories", params=kwargs)
        return [SolutionCategory.model_validate(c) for c in res]

    def view_category(self, id: int) -> SolutionCategory:
        res = self._client.request("GET", f"solutions/categories/{id}")
        return SolutionCategory.model_validate(res)

    def create_category(self, **kwargs: Any) -> SolutionCategory:
        res = self._client.request("POST", "solutions/categories", json=kwargs)
        return SolutionCategory.model_validate(res)

    def update_category(self, id: int, **kwargs: Any) -> SolutionCategory:
        res = self._client.request("PUT", f"solutions/categories/{id}", json=kwargs)
        return SolutionCategory.model_validate(res)

    def delete_category(self, id: int) -> None:
        self._client.request("DELETE", f"solutions/categories/{id}")

    # Folders
    def list_folders(self, category_id: int, **kwargs: Any) -> List[SolutionFolder]:
        res = self._client.request("GET", f"solutions/categories/{category_id}/folders", params=kwargs)
        return [SolutionFolder.model_validate(f) for f in res]

    def view_folder(self, id: int) -> SolutionFolder:
        res = self._client.request("GET", f"solutions/folders/{id}")
        return SolutionFolder.model_validate(res)

    def create_folder(self, category_id: int, **kwargs: Any) -> SolutionFolder:
        res = self._client.request("POST", f"solutions/categories/{category_id}/folders", json=kwargs)
        return SolutionFolder.model_validate(res)

    def update_folder(self, id: int, **kwargs: Any) -> SolutionFolder:
        res = self._client.request("PUT", f"solutions/folders/{id}", json=kwargs)
        return SolutionFolder.model_validate(res)

    def delete_folder(self, id: int) -> None:
        self._client.request("DELETE", f"solutions/folders/{id}")

    # Articles
    def list_articles(self, folder_id: int, **kwargs: Any) -> List[SolutionArticle]:
        res = self._client.request("GET", f"solutions/folders/{folder_id}/articles", params=kwargs)
        return [SolutionArticle.model_validate(a) for a in res]

    def view_article(self, id: int) -> SolutionArticle:
        res = self._client.request("GET", f"solutions/articles/{id}")
        return SolutionArticle.model_validate(res)

    def create_article(self, folder_id: int, **kwargs: Any) -> SolutionArticle:
        res = self._client.request("POST", f"solutions/folders/{folder_id}/articles", json=kwargs)
        return SolutionArticle.model_validate(res)

    def update_article(self, id: int, **kwargs: Any) -> SolutionArticle:
        res = self._client.request("PUT", f"solutions/articles/{id}", json=kwargs)
        return SolutionArticle.model_validate(res)

    def delete_article(self, id: int) -> None:
        self._client.request("DELETE", f"solutions/articles/{id}")

    def search_articles(self, keyword: str) -> List[SolutionArticle]:
        res = self._client.request("GET", "search/solutions", params={"keyword": keyword})
        return [SolutionArticle.model_validate(a) for a in res]


class AsyncSolutionsAPI:
    """Asynchronous implementation of the Solutions API."""
    def __init__(self, client: AsyncFreshdesk):
        self._client = client

    # Categories
    async def list_categories(self, **kwargs: Any) -> List[SolutionCategory]:
        res = await self._client.request("GET", "solutions/categories", params=kwargs)
        return [SolutionCategory.model_validate(c) for c in res]

    async def view_category(self, id: int) -> SolutionCategory:
        res = await self._client.request("GET", f"solutions/categories/{id}")
        return SolutionCategory.model_validate(res)

    async def create_category(self, **kwargs: Any) -> SolutionCategory:
        res = await self._client.request("POST", "solutions/categories", json=kwargs)
        return SolutionCategory.model_validate(res)

    async def update_category(self, id: int, **kwargs: Any) -> SolutionCategory:
        res = await self._client.request("PUT", f"solutions/categories/{id}", json=kwargs)
        return SolutionCategory.model_validate(res)

    async def delete_category(self, id: int) -> None:
        await self._client.request("DELETE", f"solutions/categories/{id}")

    # Folders
    async def list_folders(self, category_id: int, **kwargs: Any) -> List[SolutionFolder]:
        res = await self._client.request("GET", f"solutions/categories/{category_id}/folders", params=kwargs)
        return [SolutionFolder.model_validate(f) for f in res]

    async def view_folder(self, id: int) -> SolutionFolder:
        res = await self._client.request("GET", f"solutions/folders/{id}")
        return SolutionFolder.model_validate(res)

    async def create_folder(self, category_id: int, **kwargs: Any) -> SolutionFolder:
        res = await self._client.request("POST", f"solutions/categories/{category_id}/folders", json=kwargs)
        return SolutionFolder.model_validate(res)

    async def update_folder(self, id: int, **kwargs: Any) -> SolutionFolder:
        res = await self._client.request("PUT", f"solutions/folders/{id}", json=kwargs)
        return SolutionFolder.model_validate(res)

    async def delete_folder(self, id: int) -> None:
        await self._client.request("DELETE", f"solutions/folders/{id}")

    # Articles
    async def list_articles(self, folder_id: int, **kwargs: Any) -> List[SolutionArticle]:
        res = await self._client.request("GET", f"solutions/folders/{folder_id}/articles", params=kwargs)
        return [SolutionArticle.model_validate(a) for a in res]

    async def view_article(self, id: int) -> SolutionArticle:
        res = await self._client.request("GET", f"solutions/articles/{id}")
        return SolutionArticle.model_validate(res)

    async def create_article(self, folder_id: int, **kwargs: Any) -> SolutionArticle:
        res = await self._client.request("POST", f"solutions/folders/{folder_id}/articles", json=kwargs)
        return SolutionArticle.model_validate(res)

    async def update_article(self, id: int, **kwargs: Any) -> SolutionArticle:
        res = await self._client.request("PUT", f"solutions/articles/{id}", json=kwargs)
        return SolutionArticle.model_validate(res)

    async def delete_article(self, id: int) -> None:
        await self._client.request("DELETE", f"solutions/articles/{id}")

    async def search_articles(self, keyword: str) -> List[SolutionArticle]:
        res = await self._client.request("GET", "search/solutions", params={"keyword": keyword})
        return [SolutionArticle.model_validate(a) for a in res]
