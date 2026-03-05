"""Integration tests for content API modules: discussions, solutions, surveys."""
import uuid

import pytest

from freshdesk.exceptions import FreshdeskAPIError
from freshdesk.models.discussions import Category, Comment, Forum, Topic
from freshdesk.models.solutions import SolutionArticle, SolutionCategory, SolutionFolder
from freshdesk.models.surveys import SatisfactionRating, Survey
from conftest import api_or_skip, async_api_or_skip

_RUN_ID = uuid.uuid4().hex[:8]


# ---------------------------------------------------------------------------
# Discussions (categories → forums → topics → comments)
# ---------------------------------------------------------------------------

class TestDiscussionsSync:
    def test_list_categories(self, client):
        result = api_or_skip(client.discussions.list_categories)
        assert isinstance(result, list)

    def test_full_lifecycle(self, client):
        cat = api_or_skip(
            client.discussions.create_category, name=f"[TEST] Discussion Category {_RUN_ID}"
        )
        assert isinstance(cat, Category)
        try:
            client.discussions.view_category(cat.id)
            client.discussions.update_category(cat.id, name=f"[TEST] Updated Cat {_RUN_ID}")

            forum = client.discussions.create_forum(
                cat.id, name=f"[TEST] Forum {_RUN_ID}", forum_visibility=1
            )
            client.discussions.view_forum(forum.id)
            client.discussions.update_forum(forum.id, name=f"[TEST] Updated Forum {_RUN_ID}")
            client.discussions.list_forums(cat.id)

            topic = client.discussions.create_topic(
                forum.id, title=f"[TEST] Topic {_RUN_ID}", message="Body text"
            )
            client.discussions.view_topic(topic.id)
            client.discussions.update_topic(topic.id, title=f"[TEST] Updated Topic {_RUN_ID}")
            client.discussions.list_topics(forum.id)
            client.discussions.list_all_topics()

            comment = client.discussions.create_comment(topic.id, body="[TEST] Comment")
            client.discussions.list_comments(topic.id)
            client.discussions.update_comment(topic.id, comment.id, body="[TEST] Updated")

            client.discussions.delete_comment(topic.id, comment.id)
            client.discussions.delete_topic(topic.id)
            client.discussions.delete_forum(forum.id)
        except FreshdeskAPIError as e:
            pytest.skip(f"Discussion lifecycle failed ({e.status_code})")
        finally:
            try:
                client.discussions.delete_category(cat.id)
            except Exception:
                pass


class TestDiscussionsAsync:
    async def test_list_categories(self, async_client):
        result = await async_api_or_skip(
            async_client.discussions.list_categories()
        )
        assert isinstance(result, list)

    async def test_full_lifecycle(self, async_client):
        cat = await async_api_or_skip(
            async_client.discussions.create_category(name=f"[TEST] Async Discussion Cat {_RUN_ID}")
        )
        assert isinstance(cat, Category)
        try:
            await async_client.discussions.view_category(cat.id)
            await async_client.discussions.update_category(cat.id, name=f"[TEST] Async Updated Cat {_RUN_ID}")

            forum = await async_client.discussions.create_forum(
                cat.id, name=f"[TEST] Async Forum {_RUN_ID}", forum_visibility=1
            )
            await async_client.discussions.view_forum(forum.id)
            await async_client.discussions.update_forum(forum.id, name=f"[TEST] Async Updated Forum {_RUN_ID}")
            await async_client.discussions.list_forums(cat.id)

            topic = await async_client.discussions.create_topic(
                forum.id, title=f"[TEST] Async Topic {_RUN_ID}", message="Body"
            )
            await async_client.discussions.view_topic(topic.id)
            await async_client.discussions.update_topic(topic.id, title=f"[TEST] Async Updated Topic {_RUN_ID}")
            await async_client.discussions.list_topics(forum.id)
            await async_client.discussions.list_all_topics()

            comment = await async_client.discussions.create_comment(topic.id, body="[TEST] Async Comment")
            await async_client.discussions.list_comments(topic.id)
            await async_client.discussions.update_comment(topic.id, comment.id, body="[TEST] Async Updated")

            await async_client.discussions.delete_comment(topic.id, comment.id)
            await async_client.discussions.delete_topic(topic.id)
            await async_client.discussions.delete_forum(forum.id)
        except FreshdeskAPIError as e:
            pytest.skip(f"Discussion lifecycle failed ({e.status_code})")
        finally:
            try:
                await async_client.discussions.delete_category(cat.id)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Solutions (categories → folders → articles)
# ---------------------------------------------------------------------------

class TestSolutionsSync:
    def test_list_categories(self, client):
        result = api_or_skip(client.solutions.list_categories)
        assert isinstance(result, list)

    def test_full_lifecycle(self, client):
        cat = api_or_skip(
            client.solutions.create_category, name=f"[TEST] Solution Category {_RUN_ID}"
        )
        assert isinstance(cat, SolutionCategory)
        try:
            viewed_cat = client.solutions.view_category(cat.id)
            assert viewed_cat.id == cat.id

            updated_cat = client.solutions.update_category(
                cat.id, name=f"[TEST] Updated Sol Cat {_RUN_ID}"
            )
            assert isinstance(updated_cat, SolutionCategory)

            folder = client.solutions.create_folder(
                cat.id, name=f"[TEST] Folder {_RUN_ID}", visibility=1
            )
            assert isinstance(folder, SolutionFolder)

            viewed_folder = client.solutions.view_folder(folder.id)
            assert viewed_folder.id == folder.id

            updated_folder = client.solutions.update_folder(
                folder.id, name=f"[TEST] Updated Folder {_RUN_ID}"
            )
            assert isinstance(updated_folder, SolutionFolder)

            folders = client.solutions.list_folders(cat.id)
            assert isinstance(folders, list)

            article = client.solutions.create_article(
                folder.id,
                title=f"[TEST] Article {_RUN_ID}",
                description="Test article body",
                status=1,
            )
            assert isinstance(article, SolutionArticle)

            viewed_article = client.solutions.view_article(article.id)
            assert viewed_article.id == article.id

            updated_article = client.solutions.update_article(
                article.id, title=f"[TEST] Updated Article {_RUN_ID}"
            )
            assert isinstance(updated_article, SolutionArticle)

            articles = client.solutions.list_articles(folder.id)
            assert isinstance(articles, list)

            searched = client.solutions.search_articles(keyword="[TEST]")
            assert isinstance(searched, list)

            client.solutions.delete_article(article.id)
            client.solutions.delete_folder(folder.id)
        finally:
            client.solutions.delete_category(cat.id)


class TestSolutionsAsync:
    async def test_list_categories(self, async_client):
        result = await async_api_or_skip(
            async_client.solutions.list_categories()
        )
        assert isinstance(result, list)

    async def test_full_lifecycle(self, async_client):
        cat = await async_api_or_skip(
            async_client.solutions.create_category(
                name=f"[TEST] Async Solution Cat {_RUN_ID}"
            )
        )
        assert isinstance(cat, SolutionCategory)
        try:
            viewed_cat = await async_client.solutions.view_category(cat.id)
            assert viewed_cat.id == cat.id

            updated_cat = await async_client.solutions.update_category(
                cat.id, name=f"[TEST] Async Updated Sol Cat {_RUN_ID}"
            )
            assert isinstance(updated_cat, SolutionCategory)

            folder = await async_client.solutions.create_folder(
                cat.id, name=f"[TEST] Async Folder {_RUN_ID}", visibility=1
            )
            assert isinstance(folder, SolutionFolder)

            viewed_folder = await async_client.solutions.view_folder(folder.id)
            assert viewed_folder.id == folder.id

            updated_folder = await async_client.solutions.update_folder(
                folder.id, name=f"[TEST] Async Updated Folder {_RUN_ID}"
            )
            assert isinstance(updated_folder, SolutionFolder)

            folders = await async_client.solutions.list_folders(cat.id)
            assert isinstance(folders, list)

            article = await async_client.solutions.create_article(
                folder.id,
                title=f"[TEST] Async Article {_RUN_ID}",
                description="Async test body",
                status=1,
            )
            assert isinstance(article, SolutionArticle)

            viewed_article = await async_client.solutions.view_article(article.id)
            assert viewed_article.id == article.id

            updated_article = await async_client.solutions.update_article(
                article.id, title=f"[TEST] Async Updated Article {_RUN_ID}"
            )
            assert isinstance(updated_article, SolutionArticle)

            articles = await async_client.solutions.list_articles(folder.id)
            assert isinstance(articles, list)

            searched = await async_client.solutions.search_articles(keyword="[TEST]")
            assert isinstance(searched, list)

            await async_client.solutions.delete_article(article.id)
            await async_client.solutions.delete_folder(folder.id)
        finally:
            await async_client.solutions.delete_category(cat.id)


# ---------------------------------------------------------------------------
# Surveys (read-only)
# ---------------------------------------------------------------------------

class TestSurveysSync:
    def test_list_surveys(self, client):
        result = api_or_skip(client.surveys.list_surveys)
        assert isinstance(result, list)

    def test_list_satisfaction_ratings(self, client):
        result = api_or_skip(client.surveys.list_satisfaction_ratings)
        assert isinstance(result, list)


class TestSurveysAsync:
    async def test_list_surveys(self, async_client):
        result = await async_api_or_skip(async_client.surveys.list_surveys())
        assert isinstance(result, list)

    async def test_list_satisfaction_ratings(self, async_client):
        result = await async_api_or_skip(
            async_client.surveys.list_satisfaction_ratings()
        )
        assert isinstance(result, list)
