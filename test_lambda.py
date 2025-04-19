import json
import os
import unittest
from unittest.mock import patch

# Import the lambda function
import lambda_function

class TestLambdaFunction(unittest.TestCase):
    """Test cases for the Lambda function."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Set environment variables for testing
        os.environ['STAGE'] = 'test'
    
    def test_get_request_success(self):
        """Test successful GET request."""
        # Create a mock event
        event = {
            'httpMethod': 'GET',
            'pathParameters': {'userId': 'test-user'},
            'queryStringParameters': {'name': 'Test User'}
        }
        
        # Mock context
        context = {}
        
        # Call the lambda handler
        response = lambda_function.lambda_handler(event, context)
        
        # Assertions
        self.assertEqual(response['statusCode'], 200)
        
        # Parse the response body
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Hello, Test User!')
        self.assertEqual(body['user_id'], 'test-user')
        self.assertEqual(body['metadata']['stage'], 'test')
        self.assertEqual(body['metadata']['method'], 'GET')
    
    def test_post_request_success(self):
        """Test successful POST request."""
        # Create a mock event
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({
                'name': 'Test User',
                'message': 'This is a test message'
            })
        }
        
        # Mock context
        context = {}
        
        # Call the lambda handler
        response = lambda_function.lambda_handler(event, context)
        
        # Assertions
        self.assertEqual(response['statusCode'], 201)
        
        # Parse the response body
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Hello, Test User! You said: This is a test message')
        self.assertEqual(body['metadata']['stage'], 'test')
        self.assertEqual(body['metadata']['method'], 'POST')
    
    def test_invalid_method(self):
        """Test request with invalid HTTP method."""
        # Create a mock event
        event = {
            'httpMethod': 'PUT'
        }
        
        # Mock context
        context = {}
        
        # Call the lambda handler
        response = lambda_function.lambda_handler(event, context)
        
        # Assertions
        self.assertEqual(response['statusCode'], 405)
        
        # Parse the response body
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Method PUT not allowed')
    
    def test_error_handling(self):
        """Test error handling."""
        # Create a mock event that will cause an error
        event = {
            'httpMethod': 'POST',
            'body': 'invalid json'
        }
        
        # Mock context
        context = {}
        
        # Call the lambda handler
        response = lambda_function.lambda_handler(event, context)
        
        # Assertions
        self.assertEqual(response['statusCode'], 500)
        
        # Parse the response body
        body = json.loads(response['body'])
        self.assertTrue('message' in body)
        self.assertTrue('error' in body)

if __name__ == '__main__':
    unittest.main()