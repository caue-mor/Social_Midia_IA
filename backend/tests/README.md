# AgenteSocial Backend Test Suite

Comprehensive testing framework for the AgenteSocial FastAPI backend.

## Test Structure

```
tests/
├── __init__.py              # Package marker
├── conftest.py              # Pytest fixtures and configuration
├── test_health.py           # Health endpoint tests
├── test_auth.py             # Authentication system tests
├── test_chat.py             # Chat API endpoint tests
└── test_content.py          # Content generation endpoint tests
```

## Setup

### Install Test Dependencies

```bash
pip install pytest pytest-asyncio pytest-env python-jose[cryptography]
```

### Environment Configuration

Test environment variables are configured in `pyproject.toml`:
- `ENVIRONMENT=test`
- `SUPABASE_URL=http://test.supabase.co`
- `SUPABASE_KEY=test-key`
- `OPENAI_API_KEY=test-openai-key`
- `API_SECRET_KEY=test-secret`
- `SUPABASE_JWT_SECRET=test-jwt-secret`

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test
```bash
pytest tests/test_auth.py::test_jwt_auth_valid -v
```

## Test Fixtures

### `mock_env` (autouse)
Automatically sets test environment variables for all tests.

### `mock_supabase`
Provides a mocked Supabase client with chainable methods:
- `.table().select().eq().execute()`
- `.table().insert().execute()`
- `.table().update().eq().execute()`
- `.table().delete().eq().execute()`
- `.rpc().execute()`

### `client`
FastAPI TestClient with mocked Supabase dependency.

### `auth_headers`
Valid JWT Bearer token headers for authenticated requests:
```python
{"Authorization": "Bearer <valid_jwt>"}
```

### `api_key_headers`
API key headers for service-to-service authentication:
```python
{"X-API-Key": "test-secret"}
```

## Authentication System

The test suite covers both authentication methods:

### 1. JWT Authentication
```python
def test_jwt_auth_valid(client, auth_headers):
    response = client.get("/api/v1/chat/conversations", headers=auth_headers)
    assert response.status_code == 200
```

### 2. API Key Authentication
```python
def test_api_key_auth_valid(client, api_key_headers):
    response = client.get("/api/v1/chat/conversations", headers=api_key_headers)
    assert response.status_code == 200
```

## Test Categories

### Health Tests (`test_health.py`)
- Health endpoint availability
- Service metadata validation
- Health checks structure

### Auth Tests (`test_auth.py`)
- Valid JWT authentication
- Expired JWT rejection
- Valid API key authentication
- Invalid API key rejection
- No authentication rejection
- Health endpoint public access

### Chat Tests (`test_chat.py`)
- Send chat message
- Empty message validation
- List conversations

### Content Tests (`test_content.py`)
- Generate content
- Missing fields validation
- Content library listing

## Mocking Patterns

### Mock Supabase Responses
```python
def test_example(client, auth_headers, mock_supabase):
    # Configure mock response
    mock_supabase.table().select().execute.return_value = MagicMock(
        data=[{"id": "123", "name": "Test"}]
    )

    response = client.get("/api/v1/endpoint", headers=auth_headers)
    assert response.status_code == 200
```

### Mock Async Functions
```python
from unittest.mock import patch, AsyncMock

def test_example(client, auth_headers):
    with patch("app.module.async_function", new_callable=AsyncMock, return_value={"result": "ok"}):
        response = client.post("/api/v1/endpoint", headers=auth_headers)
        assert response.status_code == 200
```

## Coverage Goals

- **Unit Tests**: 70% of test suite
- **Integration Tests**: 20% of test suite
- **E2E Tests**: 10% of test suite

Target coverage thresholds:
- Branches: 80%
- Functions: 80%
- Lines: 80%
- Statements: 80%

## Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Clear Names**: Use descriptive test function names
3. **AAA Pattern**: Arrange, Act, Assert structure
4. **Mock External Deps**: Always mock Supabase, OpenAI, etc.
5. **Test Edge Cases**: Include error scenarios
6. **Use Fixtures**: Leverage pytest fixtures for reusability

## Next Steps

To expand the test suite, consider adding:

1. **Integration Tests**
   - Database integration with test DB
   - Redis integration tests
   - External API integration tests

2. **E2E Tests**
   - Complete user workflows
   - Multi-agent interactions
   - Content lifecycle tests

3. **Performance Tests**
   - Load testing with locust/k6
   - Response time benchmarks
   - Concurrent request handling

4. **Security Tests**
   - SQL injection attempts
   - XSS prevention
   - Rate limiting
   - CORS validation

## Troubleshooting

### Import Errors
If you get import errors, ensure you're running pytest from the backend directory:
```bash
cd /Users/steveherison/AgenteSocial/backend
pytest
```

### Settings Cache
The `conftest.py` fixture clears FastAPI settings cache to ensure test environment variables are used.

### Async Tests
The test suite uses `pytest-asyncio` with `asyncio_mode = "auto"` configured in `pyproject.toml`.

## Contributing

When adding new tests:

1. Follow existing naming patterns (`test_<feature>.py`)
2. Add docstrings to test functions
3. Update this README with new test categories
4. Ensure tests are independent and can run in any order
5. Mock all external dependencies
6. Test both success and failure scenarios
