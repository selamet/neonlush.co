import json
import logging
from datetime import datetime
from django.conf import settings


class LoggingService:
    """
    Service class for handling application logging
    """
    
    def __init__(self):
        self.logger = logging.getLogger('application')
    
    def log_user_action(self, user, action, details=None):
        """Log user actions"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'user': str(user),
            'action': action,
            'details': details or {}
        }
        self.logger.info(f"USER_ACTION: {json.dumps(log_data, default=str)}")
    
    def log_api_error(self, request, error, traceback_info=None):
        """Log API errors with context"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'path': request.get_full_path(),
            'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
            'error': str(error),
            'error_type': type(error).__name__,
        }
        
        if traceback_info:
            log_data['traceback'] = traceback_info
        
        self.logger.error(f"API_ERROR: {json.dumps(log_data, default=str)}")
    
    def log_business_event(self, event_type, data=None):
        """Log business events"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data or {}
        }
        self.logger.info(f"BUSINESS_EVENT: {json.dumps(log_data, default=str)}")


# Singleton instance
logging_service = LoggingService()