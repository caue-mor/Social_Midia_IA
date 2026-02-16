from unittest.mock import patch, AsyncMock


def test_send_message(client, auth_headers):
    """Test sending a chat message."""
    mock_response = {
        "response": "Ola! Como posso ajudar?",
        "conversation_id": "conv-123",
        "agent_type": "master",
        "metadata": None,
    }

    with patch("app.api.v1.chat.get_team_response", new_callable=AsyncMock, return_value=mock_response):
        response = client.post(
            "/api/v1/chat/",
            json={"message": "Ola"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Ola! Como posso ajudar?"
        assert data["conversation_id"] == "conv-123"


def test_send_message_empty(client, auth_headers):
    """Test sending empty message fails validation."""
    response = client.post(
        "/api/v1/chat/",
        json={},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_list_conversations(client, auth_headers):
    """Test listing conversations."""
    response = client.get("/api/v1/chat/conversations", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "conversations" in data
