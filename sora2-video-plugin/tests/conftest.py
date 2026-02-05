"""Pytest configuration and fixtures for sora2-video-plugin tests"""

import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_api_key():
    """Mock API Key for testing"""
    return "test_api_key_12345"


@pytest.fixture
def mock_credentials(mock_api_key):
    """Mock credentials dict"""
    return {"api_key": mock_api_key}


@pytest.fixture
def mock_runtime():
    """Mock ToolRuntime"""
    runtime = Mock()
    runtime.credentials = {"api_key": "test_api_key"}
    return runtime


@pytest.fixture
def mock_session():
    """Mock Session"""
    return Mock()


@pytest.fixture
def mock_tool_runtime(mock_api_key):
    """Mock tool runtime with credentials"""
    runtime = Mock()
    runtime.credentials = {"api_key": mock_api_key}
    return runtime


@pytest.fixture
def mock_tool_session():
    """Mock tool session"""
    return Mock()


@pytest.fixture
def mock_video_task_response():
    """Mock successful video task creation response"""
    return {
        "task_id": "test_task_123",
        "status": "pending"
    }


@pytest.fixture
def mock_video_completed_response():
    """Mock completed video task response"""
    return {
        "task_id": "test_task_123",
        "status": "completed",
        "video_url": "https://example.com/video.mp4",
        "duration": "5s"
    }


@pytest.fixture
def mock_video_processing_response():
    """Mock processing video task response"""
    return {
        "task_id": "test_task_123",
        "status": "processing"
    }


@pytest.fixture
def mock_video_failed_response():
    """Mock failed video task response"""
    return {
        "task_id": "test_task_123",
        "status": "failed",
        "error": "Generation failed"
    }


@pytest.fixture
def text_to_video_params():
    """Default text_to_video parameters"""
    return {
        "prompt": "一只可爱的橙猫在草地上奔跑",
        "model": "sora-2",
        "duration": "10",
        "aspect_ratio": "16:9"
    }


@pytest.fixture
def image_to_video_params():
    """Default image_to_video parameters"""
    return {
        "prompt": "让图片中的角色动起来",
        "images": "https://example.com/image.jpg",
        "model": "sora-2",
        "duration": "10",
        "aspect_ratio": "16:9"
    }
