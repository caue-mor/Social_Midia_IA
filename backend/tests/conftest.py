import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient
from jose import jwt
import time


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Set test environment variables."""
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("SUPABASE_URL", "http://test.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("API_SECRET_KEY", "test-secret")
    monkeypatch.setenv("SUPABASE_JWT_SECRET", "test-jwt-secret")


@pytest.fixture
def mock_supabase():
    """Mock Supabase client."""
    mock = MagicMock()
    mock_table = MagicMock()
    mock_table.select.return_value = mock_table
    mock_table.insert.return_value = mock_table
    mock_table.update.return_value = mock_table
    mock_table.delete.return_value = mock_table
    mock_table.eq.return_value = mock_table
    mock_table.gte.return_value = mock_table
    mock_table.lt.return_value = mock_table
    mock_table.order.return_value = mock_table
    mock_table.limit.return_value = mock_table
    mock_table.single.return_value = mock_table
    mock_table.maybe_single.return_value = mock_table
    mock_table.execute.return_value = MagicMock(data=[])
    mock.table.return_value = mock_table
    mock.rpc.return_value = mock_table
    return mock


@pytest.fixture
def client(mock_supabase):
    """Create test client with mocked dependencies."""
    from app.config import get_settings
    # Clear cached settings
    get_settings.cache_clear()

    with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
        from app.main import app
        with TestClient(app) as c:
            yield c

    get_settings.cache_clear()


@pytest.fixture
def auth_headers():
    """Generate valid JWT auth headers for testing."""
    payload = {
        "sub": "test-user-123",
        "email": "test@example.com",
        "role": "authenticated",
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
    }
    token = jwt.encode(payload, "test-jwt-secret", algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def api_key_headers():
    """API key auth headers for service-to-service calls."""
    return {"X-API-Key": "test-secret"}
