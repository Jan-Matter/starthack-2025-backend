from fastapi import APIRouter, Request
from typing import Dict

from api.constants import APIEndpoints
from fastapi import APIRouter, Request, Query
from typing import Dict, Optional

from api.constants import APIEndpoints
from controllers.IDChat_controller import IDChatController

class Fininfo:

    def __init__(self) -> None:
        pass
    
    def add_api_routes(self, router: APIRouter) -> None:
        router.add_api_route(APIEndpoints.FININFO.value, self.get, methods=['GET'])
    
    async def get(
        self, 
        request: Request,
        company: str = Query("Apple", description="Company name to analyze")
    ) -> Dict:
        # Create and initialize controller
        controller = IDChatController()
        try:
            await controller.initialize()
            
            result = await controller.compare_companies(["Apple", "Microsoft", "Google"], "market_cap")
            return result
        finally:
            # Ensure controller is properly closed
            await controller.close()