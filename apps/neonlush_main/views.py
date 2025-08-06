from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.logging_service.service import logging_service
import json


def index(request):
    """Simple index view"""
    return JsonResponse({'message': 'Welcome to NeonLush API'})


@csrf_exempt
@require_http_methods(["POST"])
def test_post(request):
    """Test POST endpoint for logging"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        
        # Log business event
        logging_service.log_business_event('test_post_received', {'data': data})
        
        return JsonResponse({
            'status': 'success',
            'received_data': data,
            'message': 'Data received and logged successfully'
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@require_http_methods(["GET"])
def test_get(request):
    """Test GET endpoint for logging"""
    logging_service.log_business_event('test_get_received', {
        'query_params': dict(request.GET)
    })
    
    return JsonResponse({
        'status': 'success',
        'message': 'GET request logged successfully',
        'query_params': dict(request.GET)
    })
