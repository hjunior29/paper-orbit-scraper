from typing import Any, Optional

def create_response(code: int, message: str, data: Optional[Any] = None) -> dict:
    """
    Create a standardized JSON response.
    
    Args:
        code (int): HTTP status code
        message (str): Response message
        data (Optional[Any]): Response data
    
    Returns:
        dict: Standardized response format
    """
    response = {
        "code": code,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    return response