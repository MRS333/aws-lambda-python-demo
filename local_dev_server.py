import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from io import BytesIO
import logging

# Import the Lambda function handler
import lambda_function

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LambdaHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler that converts requests to Lambda event format."""
    
    def _set_response(self, status_code, headers):
        """Set the response headers."""
        self.send_response(status_code)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()
    
    def _get_body(self):
        """Get the request body."""
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length).decode('utf-8')
    
    def _parse_path(self):
        """Parse the path to extract path parameters and query parameters."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Extract path parameters (for this simple example, we'll consider anything after the first path component)
        path_parts = path.strip('/').split('/')
        path_params = {}
        if len(path_parts) > 1 and path_parts[0] == 'users':
            path_params['userId'] = path_parts[1]
        
        # Extract query parameters
        query_params = {}
        if parsed_url.query:
            query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
        
        return path, path_params, query_params
    
    def _handle_request(self, http_method):
        """Handle the request by forwarding it to the Lambda handler."""
        path, path_params, query_params = self._parse_path()
        
        # Get request body for POST, PUT, etc.
        body = None
        if http_method in ['POST', 'PUT', 'PATCH']:
            body = self._get_body()
        
        # Create a Lambda event
        event = {
            'httpMethod': http_method,
            'path': path,
            'pathParameters': path_params,
            'queryStringParameters': query_params,
            'body': body,
            'headers': dict(self.headers.items())
        }
        
        # Log the event
        logger.info(f"Processed event: {json.dumps(event)}")
        
        # Call the Lambda handler
        response = lambda_function.lambda_handler(event, {})
        
        # Extract the response details
        status_code = response.get('statusCode', 200)
        headers = response.get('headers', {})
        body = response.get('body', '')
        
        # Send the response
        self._set_response(status_code, headers)
        self.wfile.write(body.encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests."""
        self._handle_request('GET')
    
    def do_POST(self):
        """Handle POST requests."""
        self._handle_request('POST')
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self._set_response(200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        })
        self.wfile.write(b'')

def run_server(host='localhost', port=8000):
    """Run the local development server."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, LambdaHTTPRequestHandler)
    logger.info(f"Starting server on http://{host}:{port}")
    logger.info(f"Try the API with: http://{host}:{port}/users/12345?name=TestUser")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        httpd.server_close()

if __name__ == '__main__':
    # Set environment variables for local development
    os.environ['STAGE'] = 'dev'
    
    # Get port from command line if provided
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    
    run_server(port=port)