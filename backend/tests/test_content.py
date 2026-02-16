from unittest.mock import patch, AsyncMock


def test_generate_content(client, auth_headers):
    """Test content generation endpoint."""
    mock_response = {
        "response": "Post gerado com sucesso!",
        "conversation_id": "content-123",
        "agent_type": "content_writer",
        "metadata": {"content_type": "post", "platform": "instagram"},
    }

    with patch("app.api.v1.content.get_team_response", new_callable=AsyncMock, return_value=mock_response):
        response = client.post(
            "/api/v1/content/generate",
            json={
                "content_type": "post",
                "platform": "instagram",
                "topic": "Marketing digital",
                "tone": "casual",
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["content_type"] == "post"
        assert data["platform"] == "instagram"
        assert data["body"] == "Post gerado com sucesso!"


def test_generate_content_missing_fields(client, auth_headers):
    """Test content generation with missing required fields."""
    response = client.post(
        "/api/v1/content/generate",
        json={"content_type": "post"},  # Missing platform
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_content_library(client, auth_headers):
    """Test listing content library."""
    response = client.get("/api/v1/content/library", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
