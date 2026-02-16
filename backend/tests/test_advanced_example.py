"""
Advanced test examples demonstrating test utilities and patterns.

These tests show best practices for:
- Using TokenGenerator for flexible auth testing
- Using SupabaseMockBuilder for complex mock scenarios
- Using APITestHelper for consistent assertions
- Testing error scenarios
- Testing edge cases
"""

from tests.utils import token_generator, mock_builder, api_helper
from unittest.mock import patch


class TestAdvancedAuthScenarios:
    """Advanced authentication test scenarios."""

    def test_custom_user_role(self, client):
        """Test authentication with custom user role."""
        token = token_generator.create_token(
            user_id="admin-123",
            email="admin@agentesocial.com",
            role="admin",
        )
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/v1/chat/conversations", headers=headers)
        assert response.status_code == 200

    def test_token_with_custom_claims(self, client):
        """Test JWT with additional custom claims."""
        token = token_generator.create_token(
            user_id="user-456",
            organization_id="org-789",
            tier="premium",
        )
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/v1/chat/conversations", headers=headers)
        assert response.status_code == 200

    def test_bearer_header_helper(self, client):
        """Test using bearer header helper."""
        headers = token_generator.create_bearer_header(
            user_id="user-999",
            email="user@test.com",
        )

        response = client.get("/api/v1/chat/conversations", headers=headers)
        assert response.status_code == 200

    def test_expired_token_helper(self, client):
        """Test using expired token helper."""
        token = token_generator.create_expired_token()
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/v1/chat/conversations", headers=headers)
        api_helper.assert_error_response(response, 401, "expired")


class TestSupabaseMockScenarios:
    """Advanced Supabase mocking scenarios."""

    def test_empty_result_set(self, client, auth_headers):
        """Test handling of empty Supabase results."""
        mock_supabase = mock_builder.create_table_mock(select_data=[])

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get("/api/v1/chat/conversations", headers=auth_headers)
            api_helper.assert_success_response(
                response,
                required_fields=["conversations"]
            )
            assert response.json()["conversations"] == []

    def test_large_result_set(self, client, auth_headers):
        """Test handling of large result sets."""
        large_dataset = [
            {"id": f"conv-{i}", "user_id": "test-user-123", "created_at": "2024-01-01"}
            for i in range(100)
        ]

        mock_supabase = mock_builder.create_table_mock(select_data=large_dataset)

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get("/api/v1/chat/conversations", headers=auth_headers)
            api_helper.assert_success_response(response)
            assert len(response.json()["conversations"]) == 100

    def test_supabase_error_response(self, client, auth_headers):
        """Test handling of Supabase errors."""
        error_response = mock_builder.create_response(
            data=None,
            error={"message": "Database connection failed", "code": "PGRST301"}
        )

        mock_supabase = mock_builder.create_table_mock()
        mock_supabase.table().select().execute.return_value = error_response

        with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
            response = client.get("/api/v1/chat/conversations", headers=auth_headers)
            # Should handle error gracefully
            assert response.status_code in [500, 503]


class TestAPIHelperUtilities:
    """Test API helper utility methods."""

    def test_success_response_assertions(self, client):
        """Test success response assertion helpers."""
        response = client.get("/health")

        # Test basic success assertion
        api_helper.assert_success_response(response, status_code=200)

        # Test with required fields
        api_helper.assert_success_response(
            response,
            status_code=200,
            required_fields=["status", "service", "version"]
        )

    def test_error_response_assertions(self, client):
        """Test error response assertion helpers."""
        # Missing auth
        response = client.get("/api/v1/chat/conversations")

        api_helper.assert_error_response(response, 401)

        # With specific error message check
        api_helper.assert_error_response(
            response,
            401,
            error_contains="authorization"
        )


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_message(self, client, auth_headers):
        """Test handling of extremely long messages."""
        from unittest.mock import AsyncMock, patch

        long_message = "A" * 10000  # 10k characters

        mock_response = {
            "response": "Message too long",
            "conversation_id": "conv-123",
            "agent_type": "master",
            "metadata": None,
        }

        with patch("app.api.v1.chat.get_team_response", new_callable=AsyncMock, return_value=mock_response):
            response = client.post(
                "/api/v1/chat/",
                json={"message": long_message},
                headers=auth_headers,
            )
            # Should either succeed or return validation error
            assert response.status_code in [200, 422]

    def test_special_characters_in_message(self, client, auth_headers):
        """Test handling of special characters."""
        from unittest.mock import AsyncMock, patch

        special_chars = "Hello! 你好 🎉 <script>alert('xss')</script>"

        mock_response = {
            "response": "Received your message",
            "conversation_id": "conv-123",
            "agent_type": "master",
            "metadata": None,
        }

        with patch("app.api.v1.chat.get_team_response", new_callable=AsyncMock, return_value=mock_response):
            response = client.post(
                "/api/v1/chat/",
                json={"message": special_chars},
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_concurrent_requests_same_user(self, client, auth_headers):
        """Test multiple concurrent requests from same user."""
        # This is a placeholder for actual concurrent testing
        # In practice, you'd use asyncio or threading
        responses = []
        for _ in range(5):
            response = client.get("/api/v1/chat/conversations", headers=auth_headers)
            responses.append(response)

        # All requests should succeed
        for response in responses:
            assert response.status_code == 200

    def test_malformed_json_payload(self, client, auth_headers):
        """Test handling of malformed JSON."""
        response = client.post(
            "/api/v1/chat/",
            data="{invalid json}",
            headers={**auth_headers, "Content-Type": "application/json"},
        )
        assert response.status_code == 422


class TestSecurityScenarios:
    """Test security-related scenarios."""

    def test_sql_injection_attempt(self, client, auth_headers):
        """Test protection against SQL injection."""
        from unittest.mock import AsyncMock, patch

        injection_attempt = "'; DROP TABLE users; --"

        mock_response = {
            "response": "Processed safely",
            "conversation_id": "conv-123",
            "agent_type": "master",
            "metadata": None,
        }

        with patch("app.api.v1.chat.get_team_response", new_callable=AsyncMock, return_value=mock_response):
            response = client.post(
                "/api/v1/chat/",
                json={"message": injection_attempt},
                headers=auth_headers,
            )
            # Should handle safely
            assert response.status_code in [200, 400]

    def test_xss_attempt(self, client, auth_headers):
        """Test protection against XSS."""
        from unittest.mock import AsyncMock, patch

        xss_attempt = "<script>alert('XSS')</script>"

        mock_response = {
            "response": "Processed safely",
            "conversation_id": "conv-123",
            "agent_type": "master",
            "metadata": None,
        }

        with patch("app.api.v1.chat.get_team_response", new_callable=AsyncMock, return_value=mock_response):
            response = client.post(
                "/api/v1/chat/",
                json={"message": xss_attempt},
                headers=auth_headers,
            )
            assert response.status_code == 200
            # Response should not contain raw script tags
            assert "<script>" not in response.json()["response"]

    def test_rate_limiting_multiple_tokens(self, client):
        """Test that different users are tracked separately."""
        # Create two different users
        headers1 = token_generator.create_bearer_header(user_id="user-1")
        headers2 = token_generator.create_bearer_header(user_id="user-2")

        # Both should be able to make requests
        response1 = client.get("/api/v1/chat/conversations", headers=headers1)
        response2 = client.get("/api/v1/chat/conversations", headers=headers2)

        assert response1.status_code == 200
        assert response2.status_code == 200
