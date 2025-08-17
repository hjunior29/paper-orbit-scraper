from app.services.hello_service import HelloService

class HelloHandler:
    def __init__(self):
        self.hello_service = HelloService()
    
    async def get_hello(self):
        return await self.hello_service.get_hello_message()