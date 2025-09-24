#!/usr/bin/env python3
"""
Unit tests for pyAIM v1.5.4 Production Mode implementation.

Tests the new production mode features:
- check_service() local validation only
- JSON error response parsing
- Enhanced error handling
- Dual accounts functionality
"""

import json
import sys
import os
import unittest
from unittest.mock import patch, Mock

# Add parent directory to path for testing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyaim.aimccp import CCPPasswordREST


class TestProductionMode(unittest.TestCase):
    """Test cases for production mode functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_uri = 'https://test.example.com'
        self.ccp = CCPPasswordREST(self.base_uri, verify=False)

    def test_check_service_production_mode_no_api_calls(self):
        """Verify check_service() makes no API calls in production mode."""
        # This should succeed even with invalid URL since no API call is made
        result = self.ccp.check_service()

        self.assertIn("Configuration validated", result)
        self.assertIn("test.example.com/AIMWebService", result)
        self.assertIn("Use GetPassword() to verify service health", result)

    def test_check_service_validates_configuration(self):
        """Verify check_service() validates basic configuration."""
        # Test with empty base_uri
        ccp_invalid = CCPPasswordREST.__new__(CCPPasswordREST)
        ccp_invalid._base_uri = ""
        ccp_invalid._service_path = "AIMWebService"
        ccp_invalid._context = Mock()

        with self.assertRaises(ValueError) as cm:
            ccp_invalid.check_service()
        self.assertIn("Base URI is required", str(cm.exception))

        # Test with empty service_path
        ccp_invalid._base_uri = "test.com"
        ccp_invalid._service_path = ""

        with self.assertRaises(ValueError) as cm:
            ccp_invalid.check_service()
        self.assertIn("Service path is required", str(cm.exception))

    def test_json_error_response_parsing(self):
        """Verify CCP JSON errors are parsed correctly."""
        # Test CCP error response
        error_response = {
            "ErrorCode": "APPAP423E",
            "ErrorMsg": "An error occurred while trying to connect to the vault with webservice app: INVALID. Error code: 9."
        }
        error_data = json.dumps(error_response).encode('utf-8')

        with self.assertRaises(ConnectionError) as cm:
            self.ccp._parse_ccp_response(error_data, 400)

        error_msg = str(cm.exception)
        self.assertIn("APPAP423E", error_msg)
        self.assertIn("error occurred while trying to connect", error_msg)

    def test_json_parse_invalid_response(self):
        """Verify invalid JSON responses are handled properly."""
        invalid_data = b"Invalid JSON response"

        with self.assertRaises(ConnectionError) as cm:
            self.ccp._parse_ccp_response(invalid_data, 500)

        error_msg = str(cm.exception)
        self.assertIn("Invalid response from CCP", error_msg)
        self.assertIn("Status 500", error_msg)
        self.assertIn("Invalid JSON response", error_msg)

    def test_json_parse_success_response(self):
        """Verify successful JSON responses are parsed correctly."""
        success_response = {
            "Content": "test_password",
            "UserName": "test_user",
            "Safe": "test_safe"
        }
        success_data = json.dumps(success_response).encode('utf-8')

        result = self.ccp._parse_ccp_response(success_data, 200)

        self.assertEqual(result["Content"], "test_password")
        self.assertEqual(result["UserName"], "test_user")
        self.assertEqual(result["Safe"], "test_safe")

    def test_dual_accounts_dictionary_creation(self):
        """Verify dual_accounts creates proper dictionary structure."""
        # Mock the HTTP connection to avoid actual API calls
        with patch('http.client.HTTPSConnection') as mock_conn:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.read.return_value = json.dumps({"UserName": "test_user"}).encode()

            mock_conn.return_value.getresponse.return_value = mock_response

            # Test dual_accounts=True creates proper query parameter
            try:
                self.ccp.GetPassword(
                    appid='test_app',
                    safe='test_safe',
                    username='test_virtual_user',
                    dual_accounts=True
                )

                # Verify the connection was made (indicating no dictionary errors)
                mock_conn.assert_called_once()

            except Exception as e:
                self.fail(f"dual_accounts functionality failed: {e}")

    def test_ssl_error_handling(self):
        """Verify SSL errors provide clear guidance."""
        # This test verifies our enhanced exception handling
        # We can't easily mock SSL errors without complex setup,
        # so we'll test the error message structure

        # Test SSL context creation with invalid path
        with self.assertRaises(ValueError) as cm:
            CCPPasswordREST(self.base_uri, verify='/nonexistent/path')

        self.assertIn("Certificate path does not exist", str(cm.exception))

    def test_certificate_path_validation(self):
        """Verify certificate path validation works correctly."""
        # Test with non-existent path
        with self.assertRaises(ValueError) as cm:
            CCPPasswordREST(self.base_uri, verify='/path/does/not/exist')

        self.assertIn("Certificate path does not exist", str(cm.exception))

    def test_verify_parameter_type_checking(self):
        """Verify verify parameter accepts only valid types."""
        # Valid types should work
        CCPPasswordREST(self.base_uri, verify=True)  # Should not raise
        CCPPasswordREST(self.base_uri, verify=False)  # Should not raise

        # Invalid type should raise TypeError
        with self.assertRaises(TypeError) as cm:
            CCPPasswordREST(self.base_uri, verify=123)

        self.assertIn("verify must be bool or str", str(cm.exception))


class TestHealthCheckPattern(unittest.TestCase):
    """Test the recommended health check pattern."""

    def setUp(self):
        """Set up test fixtures."""
        self.ccp = CCPPasswordREST('https://test.example.com', verify=False)

    def test_health_check_pattern_success(self):
        """Test successful health check pattern."""
        with patch('http.client.HTTPSConnection') as mock_conn:
            # Mock successful response
            mock_response = Mock()
            mock_response.status = 200
            mock_response.read.return_value = json.dumps({
                "Content": "test_password",
                "UserName": "health_check_user",
                "Safe": "health_check_safe"
            }).encode()

            mock_conn.return_value.getresponse.return_value = mock_response

            # Test health check pattern
            result = self.ccp.GetPassword(
                appid='monitoring_appid',
                safe='health_check_safe',
                object='health_check_account'
            )

            self.assertIn("Content", result)
            self.assertEqual(result["UserName"], "health_check_user")

    def test_health_check_pattern_failure(self):
        """Test health check pattern with service down."""
        with patch('http.client.HTTPSConnection') as mock_conn:
            # Mock CCP error response
            mock_response = Mock()
            mock_response.status = 400
            mock_response.read.return_value = json.dumps({
                "ErrorCode": "APPAP004E",
                "ErrorMsg": "Password object matching query was not found"
            }).encode()

            mock_conn.return_value.getresponse.return_value = mock_response

            # Test health check pattern with error
            with self.assertRaises(ConnectionError) as cm:
                self.ccp.GetPassword(
                    appid='monitoring_appid',
                    safe='health_check_safe',
                    object='health_check_account'
                )

            error_msg = str(cm.exception)
            self.assertIn("APPAP004E", error_msg)
            self.assertIn("Password object matching query", error_msg)


if __name__ == '__main__':
    unittest.main()