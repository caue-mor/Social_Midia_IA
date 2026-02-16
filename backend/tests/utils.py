"""
Test utilities and helper functions for AgenteSocial test suite.
"""

import time
from typing import Dict, Any, Optional
from jose import jwt
from unittest.mock import MagicMock


class TokenGenerator:
    """Helper class for generating test JWT tokens."""

    def __init__(self, secret: str = "test-jwt-secret"):
        self.secret = secret

    def create_token(
        self,
        user_id: str = "test-user-123",
        email: str = "test@example.com",
        role: str = "authenticated",
        exp_delta: int = 3600,
        **extra_claims
    ) -> str:
        """
        Create a JWT token for testing.

        Args:
            user_id: User ID to include in sub claim
            email: User email
            role: User role
            exp_delta: Expiration time in seconds from now (negative for expired)
            **extra_claims: Additional claims to include

        Returns:
            Encoded JWT token string
        """
        payload = {
            "sub": user_id,
            "email": email,
            "role": role,
            "aud": "authenticated",
            "exp": int(time.time()) + exp_delta,
            "iat": int(time.time()),
            **extra_claims,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def create_expired_token(self, **kwargs) -> str:
        """Create an expired JWT token."""
        return self.create_token(exp_delta=-3600, **kwargs)

    def create_bearer_header(self, token: Optional[str] = None, **kwargs) -> Dict[str, str]:
        """
        Create Bearer authorization header.

        Args:
            token: JWT token string (if None, generates new token)
            **kwargs: Arguments passed to create_token if token is None

        Returns:
            Dictionary with Authorization header
        """
        if token is None:
            token = self.create_token(**kwargs)
        return {"Authorization": f"Bearer {token}"}


class SupabaseMockBuilder:
    """Builder for creating Supabase mock responses."""

    @staticmethod
    def create_response(data: Any = None, error: Any = None, count: Optional[int] = None):
        """
        Create a Supabase response mock.

        Args:
            data: Response data
            error: Error object (if any)
            count: Row count for queries

        Returns:
            MagicMock object with data, error, and count attributes
        """
        response = MagicMock()
        response.data = data if data is not None else []
        response.error = error
        response.count = count
        return response

    @staticmethod
    def create_table_mock(select_data: Any = None, insert_data: Any = None):
        """
        Create a chainable Supabase table mock.

        Args:
            select_data: Default data for select queries
            insert_data: Default data for insert operations

        Returns:
            MagicMock with chainable methods
        """
        mock = MagicMock()
        mock_chain = MagicMock()

        # Setup chainable methods
        for method in ['select', 'insert', 'update', 'delete', 'eq', 'neq',
                       'gt', 'gte', 'lt', 'lte', 'like', 'ilike', 'is_', 'in_',
                       'contains', 'order', 'limit', 'range', 'single',
                       'maybe_single']:
            setattr(mock_chain, method, MagicMock(return_value=mock_chain))

        # Setup execute method
        mock_chain.execute.return_value = SupabaseMockBuilder.create_response(
            data=select_data
        )

        # Setup table method
        mock.table.return_value = mock_chain
        return mock


class APITestHelper:
    """Helper class for API testing utilities."""

    @staticmethod
    def assert_error_response(
        response,
        status_code: int,
        error_contains: Optional[str] = None
    ):
        """
        Assert that response is an error with expected format.

        Args:
            response: FastAPI test response
            status_code: Expected status code
            error_contains: Optional substring that should be in error message
        """
        assert response.status_code == status_code
        data = response.json()
        assert "detail" in data or "error" in data

        if error_contains:
            error_msg = data.get("detail", data.get("error", ""))
            assert error_contains.lower() in str(error_msg).lower()

    @staticmethod
    def assert_success_response(
        response,
        status_code: int = 200,
        required_fields: Optional[list] = None
    ):
        """
        Assert that response is successful with expected format.

        Args:
            response: FastAPI test response
            status_code: Expected status code
            required_fields: List of field names that must be present
        """
        assert response.status_code == status_code
        data = response.json()

        if required_fields:
            for field in required_fields:
                assert field in data, f"Required field '{field}' missing from response"

    @staticmethod
    def create_multipart_file(
        content: bytes,
        filename: str = "test.txt",
        content_type: str = "text/plain"
    ) -> tuple:
        """
        Create a multipart file for upload testing.

        Args:
            content: File content as bytes
            filename: Name of the file
            content_type: MIME type

        Returns:
            Tuple suitable for files parameter in requests
        """
        return (filename, content, content_type)


# Export convenience instances
token_generator = TokenGenerator()
mock_builder = SupabaseMockBuilder()
api_helper = APITestHelper()
