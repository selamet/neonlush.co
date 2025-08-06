# Logging Service Documentation

## Overview

The logging service provides comprehensive request/response logging for the Django application. It captures HTTP request payloads and responses, providing structured logging for monitoring, debugging, and audit purposes.

## Features

- **Request Logging**: Captures HTTP method, path, user, IP address, user agent, content type, and request payload
- **Response Logging**: Captures status code, content type, response time, and response body
- **Business Event Logging**: Provides utilities for logging custom business events
- **Configurable**: Can be enabled/disabled via environment variables
- **Structured Logging**: All logs are in JSON format for easy parsing and analysis
- **File and Console Output**: Logs to both files and console

## Configuration

### Environment Variables

```bash
# Enable/disable request response logging (default: True)
REQUEST_RESPONSE_LOGGING_ENABLED=True

# Maximum response body size to log in characters (default: 10000)
MAX_RESPONSE_LOG_SIZE=10000
```

### Settings

The logging service is configured in `neonlush/settings/base.py`:

- **Middleware**: `apps.logging_service.middleware.RequestResponseLoggingMiddleware` is added to the MIDDLEWARE list
- **Logging Configuration**: Structured logging configuration with separate loggers for request/response and application events
- **Log Files**: 
  - `logs/request_response.log` - HTTP request/response logs
  - `logs/application.log` - Business events and application logs

## Usage

### Automatic Request/Response Logging

All HTTP requests and responses are automatically logged when the middleware is enabled. No additional code is required.

### Manual Business Event Logging

```python
from apps.logging_service.service import logging_service

# Log user actions
logging_service.log_user_action(user, 'login', {'ip': '127.0.0.1'})

# Log business events
logging_service.log_business_event('order_created', {'order_id': 123})

# Log API errors
try:
    # Your code here
    pass
except Exception as e:
    logging_service.log_api_error(request, e)
```

## Log Format

### Request Logs

```json
{
  "method": "POST",
  "path": "/api/test-post/",
  "user": "Anonymous",
  "remote_addr": "127.0.0.1",
  "user_agent": "curl/8.5.0",
  "content_type": "application/json",
  "payload": {
    "name": "Test User",
    "email": "test@example.com"
  }
}
```

### Response Logs

```json
{
  "request": {
    "method": "POST",
    "path": "/api/test-post/",
    "user": "Anonymous",
    "remote_addr": "127.0.0.1",
    "user_agent": "curl/8.5.0",
    "content_type": "application/json",
    "payload": {...}
  },
  "response": {
    "status_code": 200,
    "content_type": "application/json",
    "response_time_ms": 0.61,
    "response_body": {
      "status": "success",
      "message": "Data received successfully"
    }
  }
}
```

### Business Event Logs

```json
{
  "timestamp": "2025-08-06T14:50:11.432098",
  "event_type": "order_created",
  "data": {
    "order_id": 123,
    "user_id": 456
  }
}
```

## Security Considerations

- **Sensitive Data**: Be careful not to log sensitive information like passwords, tokens, or personal data
- **Response Size**: Large responses are truncated to prevent excessive log file sizes
- **Performance**: Logging adds minimal overhead but consider disabling in high-traffic production environments if needed

## Testing

Run the tests with:

```bash
python manage.py test apps.logging_service.tests
```

## Log Rotation

For production environments, consider implementing log rotation using tools like `logrotate` to manage log file sizes.

## Disabling Logging

To disable request/response logging:

1. Set environment variable: `REQUEST_RESPONSE_LOGGING_ENABLED=False`
2. Or remove the middleware from the MIDDLEWARE list in settings

## Example API Endpoints

The project includes test endpoints to demonstrate the logging functionality:

- `GET /api/test-get/` - Test GET request logging with query parameters
- `POST /api/test-post/` - Test POST request logging with JSON payload
- `GET /` - Simple index endpoint

Test with curl:

```bash
# Test GET request
curl "http://localhost:8000/api/test-get/?param1=value1"

# Test POST request
curl -X POST "http://localhost:8000/api/test-post/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com"}'
```