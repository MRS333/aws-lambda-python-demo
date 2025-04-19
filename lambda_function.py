import json
import logging
import os
from datetime import datetime

from utils.helpers import validate_request, generate_response
from models.response import ResponseModel

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Main Lambda function handler for AWS API Gateway requests.
    
    Args:
        event (dict): Event data from API Gateway
        context (object): Lambda context
        
    Returns:
        dict: API Gateway response with status code and body
    """
    logger.info("Received event: %s", json.dumps(event))
    
    try:
        # Get HTTP method and path parameters
        http_method = event.get('httpMethod', '')
        path_params = event.get('pathParameters', {}) or {}
        query_params = event.get('queryStringParameters', {}) or {}
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        
        # Get environment variables
        stage = os.environ.get('STAGE', 'dev')
        
        # Log request information
        logger.info(f"Processing {http_method} request in {stage} environment")
        
        # Validate the request
        validation_result = validate_request(event)
        if not validation_result['valid']:
            return generate_response(400, {
                'message': 'Invalid request',
                'errors': validation_result['errors']
            })
        
        # Process request based on HTTP method
        if http_method == 'GET':
            # For GET requests
            user_id = path_params.get('userId', 'anonymous')
            name = query_params.get('name', 'World')
            
            # Create response model
            response_data = ResponseModel(
                message=f"Hello, {name}!",
                timestamp=datetime.utcnow().isoformat(),
                user_id=user_id,
                metadata={
                    'stage': stage,
                    'method': http_method
                }
            ).to_dict()
            
            return generate_response(200, response_data)
            
        elif http_method == 'POST':
            # For POST requests
            name = body.get('name', 'World')
            message = body.get('message', '')
            
            # Create response model
            response_data = ResponseModel(
                message=f"Hello, {name}! You said: {message}",
                timestamp=datetime.utcnow().isoformat(),
                request_body=body,
                metadata={
                    'stage': stage,
                    'method': http_method
                }
            ).to_dict()
            
            return generate_response(201, response_data)
        
        else:
            # Method not supported
            return generate_response(405, {
                'message': f'Method {http_method} not allowed'
            })
    
    except Exception as e:
        # Log the error
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        
        # Return error response
        return generate_response(500, {
            'message': 'Internal server error',
            'error': str(e)
        })