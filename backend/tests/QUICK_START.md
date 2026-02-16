# Quick Start - Backend Testing

## Installation

```bash
cd /Users/steveherison/AgenteSocial/backend
make install
```

## Run Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Verbose output
make test-verbose

# Specific test file
make test-auth
make test-chat
make test-health
make test-content

# Watch mode (auto-rerun on changes)
make test-watch
```

## Code Quality

```bash
# Format code
make format

# Run linter
make lint

# Type checking
make type-check

# All checks
make check
```

## Quick Examples

### Write a Simple Test

```python
def test_my_endpoint(client, auth_headers):
    """Test description."""
    response = client.get("/api/v1/my-endpoint", headers=auth_headers)
    assert response.status_code == 200
```

### Use Token Generator

```python
from tests.utils import token_generator

def test_with_custom_user(client):
    headers = token_generator.create_bearer_header(
        user_id="custom-123",
        email="custom@test.com"
    )
    response = client.get("/api/v1/endpoint", headers=headers)
    assert response.status_code == 200
```

### Mock Supabase Response

```python
from tests.utils import mock_builder
from unittest.mock import patch

def test_with_data(client, auth_headers):
    mock_data = [{"id": "1", "name": "Test"}]
    mock_supabase = mock_builder.create_table_mock(select_data=mock_data)

    with patch("app.database.supabase_client.get_supabase", return_value=mock_supabase):
        response = client.get("/api/v1/endpoint", headers=auth_headers)
        assert response.status_code == 200
```

### Assert Response

```python
from tests.utils import api_helper

def test_success(client, auth_headers):
    response = client.get("/api/v1/endpoint", headers=auth_headers)
    api_helper.assert_success_response(
        response,
        status_code=200,
        required_fields=["data", "status"]
    )

def test_error(client):
    response = client.get("/api/v1/protected")
    api_helper.assert_error_response(
        response,
        status_code=401,
        error_contains="authorization"
    )
```

## Test Structure

```python
# tests/test_feature.py

from unittest.mock import patch, AsyncMock
from tests.utils import token_generator, api_helper


class TestFeatureEndpoints:
    """Group related tests in a class."""

    def test_create(self, client, auth_headers):
        """Test creation."""
        response = client.post(
            "/api/v1/feature/",
            json={"name": "Test"},
            headers=auth_headers,
        )
        api_helper.assert_success_response(response, 201)

    def test_list(self, client, auth_headers):
        """Test listing."""
        response = client.get("/api/v1/feature/", headers=auth_headers)
        assert response.status_code == 200


def test_standalone_feature(client, auth_headers):
    """Standalone test function."""
    response = client.get("/api/v1/feature/123", headers=auth_headers)
    assert response.status_code == 200
```

## Available Fixtures

- `client` - FastAPI TestClient
- `auth_headers` - Valid JWT Bearer token
- `api_key_headers` - Valid API key header
- `mock_supabase` - Mocked Supabase client
- `mock_env` - Test environment variables (auto-applied)

## Common Patterns

### Test POST Endpoint
```python
def test_create_item(client, auth_headers):
    payload = {
        "name": "Test Item",
        "description": "Test description"
    }
    response = client.post("/api/v1/items/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
```

### Test Validation
```python
def test_invalid_payload(client, auth_headers):
    response = client.post("/api/v1/items/", json={}, headers=auth_headers)
    assert response.status_code == 422  # Unprocessable Entity
```

### Test Async Functions
```python
from unittest.mock import AsyncMock, patch

def test_with_async_call(client, auth_headers):
    with patch("app.module.async_func", new_callable=AsyncMock, return_value={"result": "ok"}):
        response = client.post("/api/v1/endpoint", headers=auth_headers)
        assert response.status_code == 200
```

### Test Error Handling
```python
def test_not_found(client, auth_headers):
    response = client.get("/api/v1/items/nonexistent", headers=auth_headers)
    assert response.status_code == 404

def test_internal_error(client, auth_headers):
    with patch("app.module.function", side_effect=Exception("Test error")):
        response = client.get("/api/v1/endpoint", headers=auth_headers)
        assert response.status_code == 500
```

## Tips

1. **Always use auth_headers** for protected endpoints
2. **Mock external dependencies** (Supabase, OpenAI, etc.)
3. **Test both success and error cases**
4. **Use descriptive test names** that explain what they test
5. **Keep tests independent** - don't rely on execution order
6. **Use fixtures** to reduce code duplication
7. **Run tests before committing** - use `make check`

## Next Steps

1. Read `tests/README.md` for comprehensive documentation
2. Check `tests/test_advanced_example.py` for advanced patterns
3. Review `tests/utils.py` for all available utilities
4. Run `make test-cov` to see coverage report
5. Check `.github/workflows/backend-tests.yml` for CI/CD setup
