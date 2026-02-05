"""Tests for Sora2Provider credential validation"""

import pytest
from unittest.mock import Mock, patch
import requests

from provider.sora2 import Sora2Provider


class TestSora2Provider:
    """Test cases for Sora2Provider credential validation"""

    @pytest.fixture
    def provider(self):
        """Create a Sora2Provider instance"""
        return Sora2Provider()

    def test_validate_credentials_success(self, provider, mock_credentials):
        """Test successful credential validation"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Should not raise any exception
            provider._validate_credentials(mock_credentials)
            mock_get.assert_called_once()

    def test_validate_credentials_missing_api_key(self, provider):
        """Test validation with missing API key"""
        empty_credentials = {}

        with pytest.raises(ValueError) as exc_info:
            provider._validate_credentials(empty_credentials)

        assert "API Key is required" in str(exc_info.value)

    def test_validate_credentials_invalid_key(self, provider, mock_credentials):
        """Test validation with invalid API key (401 response)"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_get.return_value = mock_response

            with pytest.raises(ValueError) as exc_info:
                provider._validate_credentials(mock_credentials)

            assert "Invalid API Key" in str(exc_info.value)

    def test_validate_credentials_connection_error(self, provider, mock_credentials):
        """Test validation with connection error"""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.ConnectionError("Connection failed")

            with pytest.raises(ValueError) as exc_info:
                provider._validate_credentials(mock_credentials)

            assert "API connection failed" in str(exc_info.value)

    def test_validate_credentials_timeout(self, provider, mock_credentials):
        """Test validation with timeout"""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.Timeout("Request timed out")

            with pytest.raises(ValueError) as exc_info:
                provider._validate_credentials(mock_credentials)

            assert "API connection failed" in str(exc_info.value)
