"""
Test data factories for AgenteSocial.

Provides factory functions to generate test data for various models.
Useful for creating consistent test data across test files.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import uuid


class UserFactory:
    """Factory for creating test user data."""

    @staticmethod
    def create(
        user_id: Optional[str] = None,
        email: Optional[str] = None,
        role: str = "authenticated",
        **kwargs
    ) -> Dict[str, Any]:
        """Create a test user."""
        return {
            "id": user_id or str(uuid.uuid4()),
            "email": email or f"user-{uuid.uuid4().hex[:8]}@test.com",
            "role": role,
            "created_at": datetime.utcnow().isoformat(),
            **kwargs
        }

    @staticmethod
    def create_batch(count: int, **kwargs) -> List[Dict[str, Any]]:
        """Create multiple test users."""
        return [UserFactory.create(**kwargs) for _ in range(count)]


class ConversationFactory:
    """Factory for creating test conversation data."""

    @staticmethod
    def create(
        conversation_id: Optional[str] = None,
        user_id: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a test conversation."""
        return {
            "id": conversation_id or f"conv-{uuid.uuid4().hex[:12]}",
            "user_id": user_id or str(uuid.uuid4()),
            "title": title or "Test Conversation",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "message_count": 0,
            "metadata": {},
            **kwargs
        }

    @staticmethod
    def create_batch(count: int, **kwargs) -> List[Dict[str, Any]]:
        """Create multiple test conversations."""
        return [ConversationFactory.create(**kwargs) for _ in range(count)]


class MessageFactory:
    """Factory for creating test message data."""

    @staticmethod
    def create(
        message_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        content: Optional[str] = None,
        role: str = "user",
        **kwargs
    ) -> Dict[str, Any]:
        """Create a test message."""
        return {
            "id": message_id or f"msg-{uuid.uuid4().hex[:12]}",
            "conversation_id": conversation_id or f"conv-{uuid.uuid4().hex[:12]}",
            "content": content or "Test message content",
            "role": role,
            "created_at": datetime.utcnow().isoformat(),
            "metadata": {},
            **kwargs
        }

    @staticmethod
    def create_batch(count: int, **kwargs) -> List[Dict[str, Any]]:
        """Create multiple test messages."""
        return [MessageFactory.create(**kwargs) for _ in range(count)]

    @staticmethod
    def create_conversation_thread(
        message_count: int = 5,
        conversation_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Create a thread of messages for a conversation."""
        conv_id = conversation_id or f"conv-{uuid.uuid4().hex[:12]}"
        messages = []

        for i in range(message_count):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append(
                MessageFactory.create(
                    conversation_id=conv_id,
                    content=f"Message {i + 1} in thread",
                    role=role
                )
            )

        return messages


class ContentFactory:
    """Factory for creating test content data."""

    @staticmethod
    def create(
        content_id: Optional[str] = None,
        user_id: Optional[str] = None,
        content_type: str = "post",
        platform: str = "instagram",
        **kwargs
    ) -> Dict[str, Any]:
        """Create test content."""
        return {
            "id": content_id or f"content-{uuid.uuid4().hex[:12]}",
            "user_id": user_id or str(uuid.uuid4()),
            "content_type": content_type,
            "platform": platform,
            "title": "Test Content",
            "body": "This is test content body",
            "status": "draft",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "metadata": {},
            **kwargs
        }

    @staticmethod
    def create_batch(count: int, **kwargs) -> List[Dict[str, Any]]:
        """Create multiple test content items."""
        return [ContentFactory.create(**kwargs) for _ in range(count)]


class PostFactory:
    """Factory for creating test social media post data."""

    PLATFORMS = ["instagram", "facebook", "twitter", "linkedin", "tiktok"]
    TONES = ["professional", "casual", "friendly", "formal", "humorous"]
    STATUSES = ["draft", "scheduled", "published", "archived"]

    @staticmethod
    def create(
        post_id: Optional[str] = None,
        platform: Optional[str] = None,
        tone: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a test social media post."""
        return {
            "id": post_id or f"post-{uuid.uuid4().hex[:12]}",
            "platform": platform or "instagram",
            "tone": tone or "casual",
            "caption": "Test post caption",
            "hashtags": ["#test", "#socialmedia"],
            "status": "draft",
            "scheduled_for": None,
            "published_at": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            **kwargs
        }

    @staticmethod
    def create_scheduled(
        days_ahead: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a scheduled post."""
        scheduled_time = datetime.utcnow() + timedelta(days=days_ahead)
        return PostFactory.create(
            status="scheduled",
            scheduled_for=scheduled_time.isoformat(),
            **kwargs
        )

    @staticmethod
    def create_published(**kwargs) -> Dict[str, Any]:
        """Create a published post."""
        published_time = datetime.utcnow() - timedelta(hours=2)
        return PostFactory.create(
            status="published",
            published_at=published_time.isoformat(),
            **kwargs
        )


class CalendarEventFactory:
    """Factory for creating test calendar event data."""

    @staticmethod
    def create(
        event_id: Optional[str] = None,
        title: Optional[str] = None,
        start_time: Optional[datetime] = None,
        duration_minutes: int = 60,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a test calendar event."""
        start = start_time or datetime.utcnow() + timedelta(days=1)
        end = start + timedelta(minutes=duration_minutes)

        return {
            "id": event_id or f"event-{uuid.uuid4().hex[:12]}",
            "title": title or "Test Event",
            "description": "Test event description",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "type": "post",
            "platform": "instagram",
            "status": "scheduled",
            "created_at": datetime.utcnow().isoformat(),
            **kwargs
        }

    @staticmethod
    def create_week_schedule(
        events_per_day: int = 2,
        start_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Create a week's worth of scheduled events."""
        start = start_date or datetime.utcnow()
        events = []

        for day in range(7):
            for event_num in range(events_per_day):
                event_time = start + timedelta(
                    days=day,
                    hours=9 + (event_num * 4)
                )
                events.append(
                    CalendarEventFactory.create(
                        title=f"Day {day + 1} Event {event_num + 1}",
                        start_time=event_time
                    )
                )

        return events


class AnalyticsFactory:
    """Factory for creating test analytics data."""

    @staticmethod
    def create_post_metrics(
        post_id: Optional[str] = None,
        platform: str = "instagram",
        **kwargs
    ) -> Dict[str, Any]:
        """Create test post metrics."""
        return {
            "post_id": post_id or f"post-{uuid.uuid4().hex[:12]}",
            "platform": platform,
            "impressions": 1000,
            "reach": 800,
            "engagement": 150,
            "likes": 100,
            "comments": 30,
            "shares": 20,
            "saves": 25,
            "clicks": 50,
            "engagement_rate": 0.15,
            "measured_at": datetime.utcnow().isoformat(),
            **kwargs
        }

    @staticmethod
    def create_account_metrics(
        platform: str = "instagram",
        **kwargs
    ) -> Dict[str, Any]:
        """Create test account-level metrics."""
        return {
            "platform": platform,
            "followers": 10000,
            "following": 500,
            "posts": 250,
            "avg_engagement_rate": 0.12,
            "total_impressions": 50000,
            "total_reach": 35000,
            "measured_at": datetime.utcnow().isoformat(),
            **kwargs
        }


# Convenience exports
user_factory = UserFactory()
conversation_factory = ConversationFactory()
message_factory = MessageFactory()
content_factory = ContentFactory()
post_factory = PostFactory()
calendar_factory = CalendarEventFactory()
analytics_factory = AnalyticsFactory()
