import json
import logging
import os
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.test.utils import override_settings
from unittest.mock import patch, Mock
from apps.logging_service.middleware import RequestResponseLoggingMiddleware
from apps.logging_service.service import logging_service


class RequestResponseLoggingMiddlewareTest(TestCase):
    """Test the request response logging middleware"""
    
    def setUp(self):
        self.client = Client()
        self.middleware = RequestResponseLoggingMiddleware(Mock())
    
    @patch('apps.logging_service.middleware.logger')
    def test_get_request_logging(self, mock_logger):
        """Test that GET requests are logged properly"""
        response = self.client.get('/api/test-get/?param1=value1')
        
        # Check that logger.info was called
        self.assertTrue(mock_logger.info.called)
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
    
    @patch('apps.logging_service.middleware.logger')
    def test_post_request_logging(self, mock_logger):
        """Test that POST requests with payload are logged properly"""
        test_data = {'test': 'data', 'number': 123}
        
        response = self.client.post(
            '/api/test-post/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # Check that logger.info was called for both request and response
        self.assertTrue(mock_logger.info.called)
        self.assertGreaterEqual(mock_logger.info.call_count, 2)  # At least request and response
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['received_data'], test_data)
    
    def test_get_client_ip(self):
        """Test the get_client_ip method"""
        request = Mock()
        request.META = {'REMOTE_ADDR': '127.0.0.1'}
        
        ip = self.middleware.get_client_ip(request)
        self.assertEqual(ip, '127.0.0.1')
        
        # Test with X-Forwarded-For header
        request.META = {
            'HTTP_X_FORWARDED_FOR': '192.168.1.1, 10.0.0.1',
            'REMOTE_ADDR': '127.0.0.1'
        }
        
        ip = self.middleware.get_client_ip(request)
        self.assertEqual(ip, '192.168.1.1')
    
    @override_settings(REQUEST_RESPONSE_LOGGING_ENABLED=False)
    @patch('apps.logging_service.middleware.logger')
    def test_logging_disabled(self, mock_logger):
        """Test that logging can be disabled via settings"""
        response = self.client.get('/api/test-get/')
        
        # Logger should not be called when logging is disabled
        self.assertFalse(mock_logger.info.called)
        
        # But the response should still work
        self.assertEqual(response.status_code, 200)


class LoggingServiceTest(TestCase):
    """Test the logging service"""
    
    @patch('apps.logging_service.service.logging.getLogger')
    def test_log_user_action(self, mock_get_logger):
        """Test user action logging"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        service = logging_service
        service.logger = mock_logger
        
        service.log_user_action('testuser', 'login', {'ip': '127.0.0.1'})
        
        # Verify logger.info was called with correct format
        self.assertTrue(mock_logger.info.called)
        call_args = mock_logger.info.call_args[0][0]
        self.assertIn('USER_ACTION:', call_args)
        self.assertIn('testuser', call_args)
        self.assertIn('login', call_args)
    
    @patch('apps.logging_service.service.logging.getLogger')
    def test_log_business_event(self, mock_get_logger):
        """Test business event logging"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        service = logging_service
        service.logger = mock_logger
        
        service.log_business_event('order_created', {'order_id': 123})
        
        # Verify logger.info was called with correct format
        self.assertTrue(mock_logger.info.called)
        call_args = mock_logger.info.call_args[0][0]
        self.assertIn('BUSINESS_EVENT:', call_args)
        self.assertIn('order_created', call_args)
    
    @patch('apps.logging_service.service.logging.getLogger')
    def test_log_api_error(self, mock_get_logger):
        """Test API error logging"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        service = logging_service
        service.logger = mock_logger
        
        request = Mock()
        request.method = 'POST'
        request.get_full_path.return_value = '/api/test/'
        request.user.is_authenticated = True
        request.user.__str__ = Mock(return_value='testuser')
        
        error = ValueError("Test error")
        service.log_api_error(request, error)
        
        # Verify logger.error was called with correct format
        self.assertTrue(mock_logger.error.called)
        call_args = mock_logger.error.call_args[0][0]
        self.assertIn('API_ERROR:', call_args)
        self.assertIn('Test error', call_args)
        self.assertIn('ValueError', call_args)
