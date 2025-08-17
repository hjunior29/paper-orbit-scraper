from app.utils.response import create_response

class HelloService:
    def __init__(self):
        pass
    
    async def get_hello_message(self):
        return create_response(
            code=200,
            message="Success",
            data={"message": "Hello World"}
        )