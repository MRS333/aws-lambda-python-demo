class ResponseModel:
    """
    Model class for standardized API responses.
    """
    
    def __init__(self, message, timestamp, user_id=None, request_body=None, metadata=None):
        """
        Initialize the response model.
        
        Args:
            message (str): Response message
            timestamp (str): ISO formatted timestamp
            user_id (str, optional): User ID if available
            request_body (dict, optional): Original request body
            metadata (dict, optional): Additional metadata
        """
        self.message = message
        self.timestamp = timestamp
        self.user_id = user_id
        self.request_body = request_body
        self.metadata = metadata or {}
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        
        Returns:
            dict: Dictionary representation of the model
        """
        result = {
            'message': self.message,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }
        
        if self.user_id:
            result['user_id'] = self.user_id
            
        if self.request_body:
            result['request_body'] = self.request_body
            
        return result