# Tests for Dify Sora2 Video Plugin

This directory contains all test files for the sora2-video-plugin.

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_provider.py         # Provider credential validation tests
├── test_text_to_video.py    # Text-to-video tool tests
├── test_image_to_video.py   # Image-to-video tool tests
├── test_polling.py          # Polling behavior tests
├── test_utils.py            # Utility functions and helpers
└── README.md                # This file
```

## Running Tests

### Run all tests
```bash
cd sora2-video-plugin
pytest
```

### Run specific test file
```bash
pytest tests/test_provider.py
```

### Run with coverage report
```bash
pytest --cov=provider --cov=tools --cov-report=html
```

### Run specific test class
```bash
pytest tests/test_text_to_video.py::TestTextToVideoTool
```

### Run specific test method
```bash
pytest tests/test_text_to_video.py::TestTextToVideoTool::test_invoke_success
```

## Test Categories

### Unit Tests (`test_provider.py`, `test_text_to_video.py`, `test_image_to_video.py`)
- Provider credential validation
- Tool invocation with various parameters
- Error handling scenarios
- Edge cases

### Polling Tests (`test_polling.py`)
- 30-second polling interval
- 5-minute timeout behavior
- Concurrent polling
- Immediate completion scenarios

## Fixtures

Available fixtures in `conftest.py`:
- `mock_api_key` - Test API key
- `mock_credentials` - Mocked ToolProviderCredentials
- `mock_video_task_response` - Mock task creation response
- `mock_video_completed_response` - Mock completed task response
- `mock_video_processing_response` - Mock processing task response
- `mock_video_failed_response` - Mock failed task response
- `text_to_video_params` - Default text-to-video parameters
- `image_to_video_params` - Default image-to-video parameters

## Coverage Goals

- Provider validation: 100%
- Tool invoke methods: 90%+
- Polling logic: 95%+
- Error handling: 100%

## Writing New Tests

1. Add test file with `test_` prefix
2. Import necessary fixtures from `conftest.py`
3. Use `@patch` decorator to mock external API calls
4. Use `assert` statements to verify expected behavior
5. Follow naming convention: `test_<function>_<scenario>`

Example:
```python
def test_invoke_with_custom_model(tool):
    """Test invoke with sora-2-pro model"""
    with patch("tools.text_to_video.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"task_id": "task_123"}
        # ... test code ...
        assert result["model"] == "sora-2-pro"
```
