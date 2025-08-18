from typing import Any, Optional
from fastapi.responses import JSONResponse

def create_response(code: int, message: str, data: Optional[Any] = None) -> JSONResponse:
    """
    Create a standardized JSON response with proper HTTP status code.
    
    Args:
        code (int): HTTP status code
        message (str): Response message
        data (Optional[Any]): Response data
    
    Returns:
        JSONResponse: FastAPI response with proper status code
    """
    response_data = {
        "code": code,
        "message": message,
        "data": data
    }
    
    return JSONResponse(content=response_data, status_code=code)