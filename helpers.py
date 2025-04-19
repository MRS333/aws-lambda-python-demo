import json
import logging

# Configure logging
logger = logging.getLogger()

def validate_request(event):
    """
    Validates the incoming API Gateway request.
    
    Args:
        event (dict): Event data from API Gateway
        
    Returns:
        dict: Validation result with valid flag and errors
    """
    errors = []
    http_method = event.get('httpMethod', '')
    
    # Validate HTTP method
    if http_method not in ['GET', 'POST']:
        errors.append(f"Unsupported HTTP method: {http_method}")
    
    # For POST requests, validate the body
    if http_method == 'POST':
        try:
            body = json.loads(event.get('body', '{}')) if event.get('body') else {}
            
            # Check required fields
            if 'name' not in body:
                errors.append("Field 'name' is required for POST requests")
                
        except json.JSONDecodeError:
            errors.append("Invalid JSON in request body")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def generate_response(status_code, body):
    """
    Generates a formatted response for API Gateway.
    
    Args:
        status_code (int): HTTP status code
        body (dict): Response body
        
    Returns:
        dict: API Gateway response object
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST'
        },
        'body': json.dumps(body)
    }

def get_config_value(key, default=None):
    """
    Gets a configuration value from environment variables.
    
    Args:
        key (str): Configuration key
        default: Default value if key is not found
        
    Returns:
        The configuration value or default
    """
    import os
    return os.environ.get(key, default)