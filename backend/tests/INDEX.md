# Test Suite Index

Complete index of all test files and utilities in the AgenteSocial backend test suite.

## Quick Navigation

- [Getting Started](#getting-started)
- [Test Files](#test-files)
- [Utilities](#utilities)
- [Configuration](#configuration)
- [Documentation](#documentation)

## Getting Started

1. **Install dependencies**: `make install`
2. **Run all tests**: `make test`
3. **View coverage**: `make test-cov`
4. **Read quick start**: [QUICK_START.md](QUICK_START.md)

## Test Files

### Core Tests

#### `test_health.py`
Health endpoint testing.

**Tests:**
- `test_health_endpoint` - Validates health check response

**Coverage:** Health endpoint, service metadata

---

#### `test_auth.py`
Authentication system testing.

**Tests:**
- `test_jwt_auth_valid` - Valid JWT token authentication
- `test_jwt_auth_expired` - Expired token rejection
- `test_api_key_auth_valid` - Valid API key authentication
- `test_api_key_auth_invalid` - Invalid API key rejection
- `test_no_auth_rejected` - No authentication rejection
- `test_health_no_auth_required` - Health endpoint public access

**Coverage:** JWT auth, API key auth, auth fallback logic

---

#### `test_chat.py`
Chat API endpoint testing.

**Tests:**
- `test_send_message` - Send chat message
- `test_send_message_empty` - Empty message validation
- `test_list_conversations` - List user conversations

**Coverage:** Chat endpoints, message validation, conversation listing

---

#### `test_content.py`
Content generation endpoint testing.

**Tests:**
- `test_generate_content` - Content generation
- `test_generate_content_missing_fields` - Field validation
- `test_content_library` - Content library listing

**Coverage:** Content generation, validation, library access

---

### Advanced Tests

#### `test_advanced_example.py`
Advanced testing patterns and examples.

**Test Classes:**
- `TestAdvancedAuthScenarios` - Custom auth scenarios
- `TestSupabaseMockScenarios` - Complex Supabase mocking
- `TestAPIHelperUtilities` - API helper usage
- `TestEdgeCases` - Edge cases and boundaries
- `TestSecurityScenarios` - Security testing

**Coverage:**
- Custom JWT claims
- Large datasets
- Error handling
- Special characters
- SQL injection protection
- XSS protection
- Concurrent requests

---

#### `test_with_factories.py`
Examples using test data factories.

**Test Classes:**
- `TestConversationsWithFactories` - Conversation testing with factories
- `TestContentWithFactories` - Content testing with factories
- `TestCalendarWithFactories` - Calendar testing with factories
- `TestAnalyticsWithFactories` - Analytics testing with factories
- `TestUserManagementWithFactories` - User management with factories

**Coverage:**
- Factory usage patterns
- Data consistency
- Batch operations
- Custom factory data

---

## Utilities

### `conftest.py`
Pytest configuration and fixtures.

**Fixtures:**
- `mock_env` (autouse) - Test environment variables
- `mock_supabase` - Mocked Supabase client
- `client` - FastAPI TestClient
- `auth_headers` - Valid JWT Bearer token
- `api_key_headers` - Valid API key headers

**Usage:**
```python
def test_example(client, auth_headers):
    response = client.get("/api/v1/endpoint", headers=auth_headers)
    assert response.status_code == 200
```

---

### `utils.py`
Test utility classes and functions.

**Classes:**

#### `TokenGenerator`
JWT token generation for testing.

**Methods:**
- `create_token(user_id, email, role, exp_delta, **extra_claims)`
- `create_expired_token(**kwargs)`
- `create_bearer_header(token, **kwargs)`

**Usage:**
```python
from tests.utils import token_generator

headers = token_generator.create_bearer_header(user_id="user-123")
```

---

#### `SupabaseMockBuilder`
Supabase mock response builder.

**Methods:**
- `create_response(data, error, count)`
- `create_table_mock(select_data, insert_data)`

**Usage:**
```python
from tests.utils import mock_builder

mock = mock_builder.create_table_mock(select_data=[{"id": "1"}])
```

---

#### `APITestHelper`
API response assertion helpers.

**Methods:**
- `assert_error_response(response, status_code, error_contains)`
- `assert_success_response(response, status_code, required_fields)`
- `create_multipart_file(content, filename, content_type)`

**Usage:**
```python
from tests.utils import api_helper

api_helper.assert_success_response(response, 200, ["data", "status"])
```

---

### `factories.py`
Test data factories for model instances.

**Factories:**

#### `UserFactory`
- `create(**kwargs)` - Single user
- `create_batch(count, **kwargs)` - Multiple users

#### `ConversationFactory`
- `create(**kwargs)` - Single conversation
- `create_batch(count, **kwargs)` - Multiple conversations

#### `MessageFactory`
- `create(**kwargs)` - Single message
- `create_batch(count, **kwargs)` - Multiple messages
- `create_conversation_thread(count, conversation_id)` - Message thread

#### `ContentFactory`
- `create(**kwargs)` - Single content item
- `create_batch(count, **kwargs)` - Multiple content items

#### `PostFactory`
- `create(**kwargs)` - Single post
- `create_scheduled(days_ahead, **kwargs)` - Scheduled post
- `create_published(**kwargs)` - Published post

#### `CalendarEventFactory`
- `create(**kwargs)` - Single event
- `create_week_schedule(events_per_day, start_date)` - Week schedule

#### `AnalyticsFactory`
- `create_post_metrics(**kwargs)` - Post metrics
- `create_account_metrics(**kwargs)` - Account metrics

**Usage:**
```python
from tests.factories import user_factory, conversation_factory

user = user_factory.create(email="test@example.com")
conversations = conversation_factory.create_batch(5, user_id=user["id"])
```

---

## Configuration

### `pyproject.toml`
Pytest configuration section.

**Settings:**
- Test paths: `tests/`
- Async mode: `auto`
- Environment variables for tests

---

### `pytest.ini`
Additional pytest configuration.

**Settings:**
- Test discovery patterns
- Output options
- Test markers
- Coverage settings

**Markers:**
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.slow` - Slow tests
- `@pytest.mark.security` - Security tests
- `@pytest.mark.auth` - Authentication tests
- `@pytest.mark.api` - API tests

**Usage:**
```python
@pytest.mark.integration
def test_database_integration():
    pass

# Run only unit tests
# pytest -m unit
```

---

### `.coveragerc`
Coverage reporting configuration.

**Settings:**
- Source path: `app/`
- Omit patterns: tests, venv, cache
- Exclude lines: pragmas, abstract methods
- HTML report directory: `htmlcov/`

---

### `Makefile`
Test command shortcuts.

**Commands:**
- `make install` - Install dependencies
- `make test` - Run all tests
- `make test-verbose` - Verbose output
- `make test-cov` - With coverage
- `make test-watch` - Watch mode
- `make test-health` - Health tests only
- `make test-auth` - Auth tests only
- `make test-chat` - Chat tests only
- `make test-content` - Content tests only
- `make lint` - Run linter
- `make format` - Format code
- `make type-check` - Type checking
- `make check` - All checks
- `make clean` - Clean cache

---

## Documentation

### `README.md`
Comprehensive test suite documentation.

**Sections:**
- Test structure overview
- Setup instructions
- Running tests guide
- Test fixtures reference
- Authentication system
- Test categories
- Mocking patterns
- Coverage goals
- Best practices
- Next steps
- Troubleshooting

---

### `QUICK_START.md`
Quick reference guide for common tasks.

**Sections:**
- Installation
- Running tests
- Code quality commands
- Quick examples
- Common patterns
- Tips

---

### `TEST_FOUNDATION_SUMMARY.md`
Complete summary of test foundation.

**Sections:**
- Overview
- Files created
- Key features
- Usage guide
- CI/CD integration
- Test organization
- Best practices
- Next steps

---

### `INDEX.md` (this file)
Complete index of all test files and utilities.

---

## CI/CD

### `.github/workflows/backend-tests.yml`
GitHub Actions workflow for automated testing.

**Jobs:**
- `test` - Run tests with coverage
- `lint` - Code formatting and linting
- `type-check` - MyPy type checking

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Changes in `backend/` directory

---

## File Tree

```
backend/
├── tests/
│   ├── __init__.py                  # Package marker
│   ├── conftest.py                  # Fixtures
│   ├── utils.py                     # Utilities
│   ├── factories.py                 # Data factories
│   ├── test_health.py               # Health tests
│   ├── test_auth.py                 # Auth tests
│   ├── test_chat.py                 # Chat tests
│   ├── test_content.py              # Content tests
│   ├── test_advanced_example.py     # Advanced patterns
│   ├── test_with_factories.py       # Factory examples
│   ├── README.md                    # Full documentation
│   ├── QUICK_START.md               # Quick reference
│   └── INDEX.md                     # This file
├── pyproject.toml                   # Project config
├── pytest.ini                       # Pytest config
├── .coveragerc                      # Coverage config
├── Makefile                         # Test commands
└── TEST_FOUNDATION_SUMMARY.md       # Summary doc
```

---

## Test Count Summary

| File | Test Count | Type |
|------|------------|------|
| test_health.py | 1 | Unit |
| test_auth.py | 6 | Unit/Security |
| test_chat.py | 3 | API |
| test_content.py | 3 | API |
| test_advanced_example.py | 20+ | Integration/Security |
| test_with_factories.py | 15+ | Unit/Integration |
| **Total** | **48+** | Mixed |

---

## Coverage Target

- **Lines**: 80%
- **Branches**: 80%
- **Functions**: 80%
- **Statements**: 80%

Current coverage: Run `make test-cov` to view.

---

## Common Test Patterns

### 1. Simple API Test
```python
def test_endpoint(client, auth_headers):
    response = client.get("/api/v1/endpoint", headers=auth_headers)
    assert response.status_code == 200
```

### 2. With Custom Token
```python
from tests.utils import token_generator

def test_with_role(client):
    headers = token_generator.create_bearer_header(role="admin")
    response = client.get("/api/v1/admin", headers=headers)
    assert response.status_code == 200
```

### 3. With Factory Data
```python
from tests.factories import user_factory

def test_with_data(client, auth_headers):
    users = user_factory.create_batch(5)
    # Use in test
```

### 4. With Mock Response
```python
from tests.utils import mock_builder
from unittest.mock import patch

def test_with_mock(client, auth_headers):
    mock = mock_builder.create_table_mock(select_data=[{"id": "1"}])
    with patch("app.database.supabase_client.get_supabase", return_value=mock):
        response = client.get("/api/v1/endpoint", headers=auth_headers)
```

### 5. Error Assertion
```python
from tests.utils import api_helper

def test_error(client):
    response = client.get("/api/v1/protected")
    api_helper.assert_error_response(response, 401, "auth")
```

---

## Next Steps

1. Run tests: `make test`
2. Check coverage: `make test-cov`
3. Add new tests for remaining endpoints
4. Expand to integration tests
5. Add performance tests
6. Setup E2E tests

---

**Last Updated**: February 2026
**Test Framework Version**: 1.0
**Status**: Production Ready
