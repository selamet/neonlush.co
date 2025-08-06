import json
import logging
import time
from io import StringIO
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


logger = logging.getLogger('request_response')


class RequestResponseLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log HTTP request payloads and responses
    """
    
    def process_request(self, request):
        """Process incoming request and log details"""
        # Record the start time
        request._start_time = time.time()
        
        # Only log if enabled in settings
        if not getattr(settings, 'REQUEST_RESPONSE_LOGGING_ENABLED', True):
            return
        
        # Capture request data
        request_data = {
            'method': request.method,
            'path': request.get_full_path(),
            'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
            'remote_addr': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'content_type': request.META.get('CONTENT_TYPE', ''),
        }
        
        # Log request payload for POST, PUT, PATCH requests
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and hasattr(request, 'body'):
            try:
                if request.content_type and 'application/json' in request.content_type:
                    request_data['payload'] = json.loads(request.body.decode('utf-8'))
                else:
                    # For form data, convert to dict
                    request_data['payload'] = dict(request.POST)
            except (ValueError, UnicodeDecodeError) as e:
                request_data['payload'] = f"Could not parse request body: {str(e)}"
        
        # Store request data on request object for later use
        request._logged_data = request_data
        
        # Log the request
        logger.info(f"REQUEST: {json.dumps(request_data, default=str)}")
    
    def process_response(self, request, response):
        """Process outgoing response and log details"""
        # Only log if enabled in settings
        if not getattr(settings, 'REQUEST_RESPONSE_LOGGING_ENABLED', True):
            return response
        
        # Calculate response time
        response_time = None
        if hasattr(request, '_start_time'):
            response_time = round((time.time() - request._start_time) * 1000, 2)  # in milliseconds
        
        # Get request data if available
        request_data = getattr(request, '_logged_data', {})
        
        # Capture response data
        response_data = {
            'status_code': response.status_code,
            'content_type': response.get('Content-Type', ''),
            'response_time_ms': response_time,
        }
        
        # Log response payload for JSON responses (be careful with large responses)
        if response.get('Content-Type', '').startswith('application/json'):
            try:
                # Only log if response is not too large
                content = response.content.decode('utf-8')
                if len(content) < getattr(settings, 'MAX_RESPONSE_LOG_SIZE', 10000):
                    response_data['response_body'] = json.loads(content)
                else:
                    response_data['response_body'] = f"Response too large ({len(content)} chars)"
            except (ValueError, UnicodeDecodeError, AttributeError):
                response_data['response_body'] = "Could not parse response body"
        
        # Combine request and response data
        log_data = {
            'request': request_data,
            'response': response_data,
        }
        
        # Log the response
        logger.info(f"RESPONSE: {json.dumps(log_data, default=str)}")
        
        return response
    
    def get_client_ip(self, request):
        """Get the client IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip