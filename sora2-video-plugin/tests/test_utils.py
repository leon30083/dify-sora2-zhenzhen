"""Utility functions and shared test helpers"""

import json
from typing import Any, Dict
from unittest.mock import Mock


def create_mock_response(data: Dict[str, Any], status_code: int = 200) -> Mock:
    """Create a mock HTTP response object"""
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = data
    mock_response.text = json.dumps(data)
    return mock_response


def parse_json_message(message: str) -> Dict[str, Any]:
    """Parse JSON message from tool result"""
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        # Handle if message is wrapped in additional structure
        if "```json" in message:
            # Extract JSON from markdown code block
            start = message.find("{")
            end = message.rfind("}") + 1
            return json.loads(message[start:end])
        raise


def assert_video_result(result: Any, expected_status: str):
    """Assert common video result structure"""
    data = parse_json_message(result.message)
    assert "status" in data
    assert data["status"] == expected_status

    if expected_status == "pending":
        assert "task_id" in data
        assert "message" in data
    elif expected_status == "completed":
        assert "task_id" in data
        assert "video_url" in data
        assert data["video_url"].startswith("https://")
    elif expected_status in ["timeout", "failed"]:
        assert "error" in data

    return data


class MockToolRuntime:
    """Mock tool runtime for testing"""

    def __init__(self, api_key: str = "test_api_key"):
        self.credentials = {"api_key": api_key}


class MockCredentials:
    """Mock Dify credentials object"""

    def __init__(self, api_key: str = "test_api_key"):
        self.credentials = {"api_key": api_key}
