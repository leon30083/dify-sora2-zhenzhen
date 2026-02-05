"""Integration tests with real API

These tests call the actual Zhenzhen platform API.
Run with: pytest tests/test_integration.py --integration
"""

import os
import pytest
import time
import requests
from tools.text_to_video import TextToVideoTool
from tools.image_to_video import ImageToVideoTool
from unittest.mock import Mock


# Test credentials from environment or use provided defaults
TEST_API_KEY = os.getenv("SORA2_API_KEY", "sk-2TqUEzLnk28nJzvXBRPlMX25a1F23hYXZy0BlRxDtWE4Kcn0")
TEST_IMAGE_URL = os.getenv(
    "TEST_IMAGE_URL",
    "https://lowly-rain-658.notion.site/image/attachment%3A2a817484-73a6-474a-a7ea-ca013e594c3d%3A3.jpg?table=block&id=2d8a3f92-69aa-8036-8f5b-fadc62538c98&spaceId=86aa3f92-69aa-81db-ab3d-00033d2c4978&width=2000&userId=&cache=v2"
)


def _create_mock_runtime(api_key: str):
    """Create mock runtime with API key"""
    runtime = Mock()
    runtime.credentials = {"api_key": api_key}
    return runtime


def _create_mock_session():
    """Create mock session"""
    return Mock()


@pytest.mark.integration
class TestRealAPITextToVideo:
    """Integration tests for text-to-video with real API"""

    def test_text_to_video_simple(self):
        """Test simple text-to-video generation"""
        tool = TextToVideoTool(_create_mock_runtime(TEST_API_KEY), _create_mock_session())

        params = {
            "prompt": "A cute orange cat running on grass",
            "model": "sora-2",
            "duration": "10",
            "aspect_ratio": "16:9"
        }

        results = list(tool._invoke(params))

        # Should have at least 2 results: pending and completed/timeout
        assert len(results) >= 1

        # Check first result (pending)
        pending_data = eval(results[0].message)
        assert "task_id" in pending_data
        assert "status" in pending_data
        print(f"Task ID: {pending_data['task_id']}")

        # Note: Real video generation can take 1-3 minutes
        # The poll_until_complete will timeout after 5 minutes
        if len(results) > 1:
            final_data = eval(results[-1].message)
            print(f"Final status: {final_data.get('status')}")
            if final_data.get("status") == "completed":
                assert "video_url" in final_data

    def test_text_to_video_pro_model(self):
        """Test text-to-video with sora-2-pro model"""
        tool = TextToVideoTool(_create_mock_runtime(TEST_API_KEY), _create_mock_session())

        params = {
            "prompt": "A sunset over the ocean",
            "model": "sora-2-pro",
            "duration": "10",
            "aspect_ratio": "16:9"
        }

        results = list(tool._invoke(params))
        assert len(results) >= 1

        pending_data = eval(results[0].message)
        assert "task_id" in pending_data
        print(f"Pro Model Task ID: {pending_data['task_id']}")


@pytest.mark.integration
class TestRealAPIImageToVideo:
    """Integration tests for image-to-video with real API"""

    def test_image_to_video_simple(self):
        """Test simple image-to-video generation"""
        tool = ImageToVideoTool(_create_mock_runtime(TEST_API_KEY), _create_mock_session())

        params = {
            "prompt": "Make the character animate",
            "images": TEST_IMAGE_URL,
            "model": "sora-2",
            "duration": "10",
            "aspect_ratio": "16:9"
        }

        results = list(tool._invoke(params))

        assert len(results) >= 1
        pending_data = eval(results[0].message)
        assert "task_id" in pending_data
        print(f"Image-to-Video Task ID: {pending_data['task_id']}")

        if len(results) > 1:
            final_data = eval(results[-1].message)
            print(f"Final status: {final_data.get('status')}")


@pytest.mark.integration
class TestRealAPIDirect:
    """Direct API tests without tool wrapper"""

    def test_direct_api_text_to_video(self):
        """Test API directly for text-to-video"""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        params = {
            "prompt": "A red car driving on a road",
            "model": "sora-2",
            "duration": "10",
            "aspect_ratio": "16:9"
        }

        # Create task
        response = requests.post(
            "https://gpt-best.apifox.cn/v2/videos/generations",
            headers=headers,
            json=params,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        task_id = data["task_id"]
        print(f"Direct API Task ID: {task_id}")

        # Query task status
        response = requests.get(
            f"https://gpt-best.apifox.cn/v2/videos/generations/{task_id}",
            headers=headers,
            timeout=10
        )
        assert response.status_code == 200
        task_data = response.json()
        assert "status" in task_data
        print(f"Task status: {task_data['status']}")

    def test_direct_api_image_to_video(self):
        """Test API directly for image-to-video"""
        headers = {"Authorization": f"Bearer {TEST_API_KEY}"}
        params = {
            "prompt": "Animate this image",
            "model": "sora-2",
            "duration": "10",
            "images": [TEST_IMAGE_URL]
        }

        # Create task
        response = requests.post(
            "https://gpt-best.apifox.cn/v2/videos/generations",
            headers=headers,
            json=params,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        print(f"Direct Image API Task ID: {data['task_id']}")


@pytest.mark.integration
class TestAPIValidation:
    """Test API validation and edge cases"""

    def test_provider_validation(self):
        """Test provider credential validation"""
        from provider.sora2 import Sora2Provider

        provider = Sora2Provider()
        # This should not raise an exception
        provider._validate_credentials({"api_key": TEST_API_KEY})

    def test_invalid_api_key(self):
        """Test with invalid API key"""
        from provider.sora2 import Sora2Provider

        provider = Sora2Provider()
        with pytest.raises(ValueError):
            provider._validate_credentials({"api_key": "invalid_key"})
