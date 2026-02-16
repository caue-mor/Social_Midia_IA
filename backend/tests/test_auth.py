import time
from jose import jwt


def test_jwt_auth_valid(client, auth_headers):
    """Test valid JWT authentication works."""
    response = client.get("/api/v1/chat/conversations", headers=auth_headers)
    assert response.status_code == 200


def test_jwt_auth_expired(client):
    """Test expired JWT is rejected."""
    payload = {
        "sub": "test-user-123",
        "email": "test@example.com",
        "role": "authenticated",
        "aud": "authenticated",
        "exp": int(time.time()) - 3600,  # Expired
        "iat": int(time.time()) - 7200,
    }
    token = jwt.encode(payload, "test-jwt-secret", algorithm="HS256")
    response = client.get(
        "/api/v1/chat/conversations",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_api_key_auth_valid(client, api_key_headers):
    """Test valid API key authentication works."""
    response = client.get("/api/v1/chat/conversations", headers=api_key_headers)
    assert response.status_code == 200


def test_api_key_auth_invalid(client):
    """Test invalid API key is rejected."""
    response = client.get(
        "/api/v1/chat/conversations",
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


def test_no_auth_rejected(client):
    """Test request without auth is rejected."""
    response = client.get("/api/v1/chat/conversations")
    assert response.status_code == 401


def test_health_no_auth_required(client):
    """Test health endpoint doesn't require auth."""
    response = client.get("/health")
    assert response.status_code == 200
