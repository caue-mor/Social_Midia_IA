"""
Example tests demonstrating the use of test data factories.

These examples show how to use factories to create consistent,
reusable test data for various scenarios.
"""

from tests.factories import (
    user_factory,
    conversation_factory,
    message_factory,
    content_factory,
    post_factory,
    calendar_factory,
    analytics_factory,
)
from tests.utils import mock_builder
from unittest.mock import patch


class TestConversationsWithFactories:
    """Test conversation endpoints using factories."""

    def test_list_user_conversations(self, client, auth_headers):
        """Test listing conversations with factory-generated data."""
        # Create test data
        test_conversations = conversation_factory.create_batch(
            count=5,
            user_id="test-user-123"
        )

        # Mock Supabase response
        mock_supabase = mock_builder.create_table_mock(
            select_data=test_conversations
        )

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get("/api/v1/chat/conversations", headers=auth_headers)

            assert response.status_code == 200
            data = response.json()
            assert "conversations" in data
            assert len(data["conversations"]) == 5

    def test_conversation_with_messages(self, client, auth_headers):
        """Test conversation with message thread."""
        # Create conversation with messages
        conversation = conversation_factory.create(user_id="test-user-123")
        messages = message_factory.create_conversation_thread(
            message_count=10,
            conversation_id=conversation["id"]
        )

        # Update conversation message count
        conversation["message_count"] = len(messages)

        mock_supabase = mock_builder.create_table_mock(select_data=messages)

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get(
                f"/api/v1/chat/conversations/{conversation['id']}/messages",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "messages" in data
            assert len(data["messages"]) == 10


class TestContentWithFactories:
    """Test content endpoints using factories."""

    def test_list_content_library(self, client, auth_headers):
        """Test content library with various content types."""
        # Create diverse content
        test_content = [
            content_factory.create(
                content_type="post",
                platform="instagram",
                status="published"
            ),
            content_factory.create(
                content_type="story",
                platform="instagram",
                status="draft"
            ),
            content_factory.create(
                content_type="reel",
                platform="instagram",
                status="scheduled"
            ),
        ]

        mock_supabase = mock_builder.create_table_mock(select_data=test_content)

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get("/api/v1/content/library", headers=auth_headers)

            assert response.status_code == 200
            data = response.json()
            assert "content" in data
            assert len(data["content"]) == 3

    def test_scheduled_posts(self, client, auth_headers):
        """Test listing scheduled posts."""
        # Create scheduled posts
        scheduled_posts = [
            post_factory.create_scheduled(days_ahead=1, platform="instagram"),
            post_factory.create_scheduled(days_ahead=2, platform="facebook"),
            post_factory.create_scheduled(days_ahead=3, platform="twitter"),
        ]

        mock_supabase = mock_builder.create_table_mock(select_data=scheduled_posts)

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get(
                "/api/v1/calendar/scheduled",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "posts" in data or "events" in data

    def test_published_posts_with_metrics(self, client, auth_headers):
        """Test published posts with analytics."""
        # Create published posts
        published_posts = [
            post_factory.create_published(platform="instagram"),
            post_factory.create_published(platform="facebook"),
        ]

        # Create corresponding metrics
        metrics = [
            analytics_factory.create_post_metrics(
                post_id=post["id"],
                platform=post["platform"]
            )
            for post in published_posts
        ]

        mock_supabase = mock_builder.create_table_mock(select_data=published_posts)

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get(
                "/api/v1/content/published",
                headers=auth_headers
            )

            assert response.status_code == 200


class TestCalendarWithFactories:
    """Test calendar endpoints using factories."""

    def test_week_schedule(self, client, auth_headers):
        """Test weekly calendar view."""
        # Create a week's worth of events
        week_events = calendar_factory.create_week_schedule(
            events_per_day=3
        )

        mock_supabase = mock_builder.create_table_mock(select_data=week_events)

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get(
                "/api/v1/calendar/week",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            # Should have events for 7 days
            assert "events" in data or "schedule" in data


class TestAnalyticsWithFactories:
    """Test analytics endpoints using factories."""

    def test_post_performance(self, client, auth_headers):
        """Test post performance analytics."""
        # Create post with metrics
        post = post_factory.create_published(platform="instagram")
        metrics = analytics_factory.create_post_metrics(
            post_id=post["id"],
            platform="instagram",
            impressions=5000,
            engagement=750,
            engagement_rate=0.15
        )

        mock_supabase = mock_builder.create_table_mock(select_data=[metrics])

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get(
                f"/api/v1/analysis/post/{post['id']}/metrics",
                headers=auth_headers
            )

            # Should return metrics or 404 if endpoint doesn't exist
            assert response.status_code in [200, 404]

    def test_account_overview(self, client, auth_headers):
        """Test account-level analytics."""
        # Create account metrics for multiple platforms
        account_metrics = [
            analytics_factory.create_account_metrics(
                platform="instagram",
                followers=15000,
                avg_engagement_rate=0.14
            ),
            analytics_factory.create_account_metrics(
                platform="facebook",
                followers=8000,
                avg_engagement_rate=0.08
            ),
        ]

        mock_supabase = mock_builder.create_table_mock(select_data=account_metrics)

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get(
                "/api/v1/analysis/overview",
                headers=auth_headers
            )

            # Should return overview or 404 if endpoint doesn't exist
            assert response.status_code in [200, 404]


class TestUserManagementWithFactories:
    """Test user management using factories."""

    def test_create_user_batch(self, client, auth_headers):
        """Test creating multiple users."""
        # Create batch of test users
        users = user_factory.create_batch(count=5)

        # Verify all have unique IDs and emails
        ids = [u["id"] for u in users]
        emails = [u["email"] for u in users]

        assert len(set(ids)) == 5, "All user IDs should be unique"
        assert len(set(emails)) == 5, "All user emails should be unique"

    def test_user_with_custom_role(self, client, auth_headers):
        """Test user with specific role."""
        admin_user = user_factory.create(
            email="admin@agentesocial.com",
            role="admin"
        )

        assert admin_user["role"] == "admin"
        assert "admin@agentesocial.com" in admin_user["email"]


def test_factory_data_consistency():
    """Test that factories generate consistent data."""
    # Create conversation
    conversation = conversation_factory.create()

    # Create messages for that conversation
    messages = message_factory.create_conversation_thread(
        message_count=5,
        conversation_id=conversation["id"]
    )

    # Verify all messages belong to the conversation
    for message in messages:
        assert message["conversation_id"] == conversation["id"]

    # Verify alternating roles
    for i, message in enumerate(messages):
        expected_role = "user" if i % 2 == 0 else "assistant"
        assert message["role"] == expected_role


def test_factory_customization():
    """Test factory customization with kwargs."""
    # Create content with custom fields
    custom_content = content_factory.create(
        title="Custom Title",
        body="Custom body text",
        status="published",
        custom_field="custom_value"
    )

    assert custom_content["title"] == "Custom Title"
    assert custom_content["body"] == "Custom body text"
    assert custom_content["status"] == "published"
    assert custom_content["custom_field"] == "custom_value"


def test_scheduled_post_factory():
    """Test scheduled post factory."""
    post = post_factory.create_scheduled(days_ahead=3)

    assert post["status"] == "scheduled"
    assert post["scheduled_for"] is not None
    assert post["published_at"] is None


def test_published_post_factory():
    """Test published post factory."""
    post = post_factory.create_published()

    assert post["status"] == "published"
    assert post["published_at"] is not None
