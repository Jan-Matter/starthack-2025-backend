from fastapi import APIRouter, Request
from typing import Dict
import os
import json

from api.constants import APIEndpoints
from fastapi import APIRouter, Request, Query
from typing import Dict, Optional

from api.constants import APIEndpoints
from controllers.IDChat_controller import IDChatController


def read_file(file_path: str) -> Dict:
    """Read and parse a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)
        
class Fininfo:

    def __init__(self) -> None:
        pass
    
    def add_api_routes(self, router: APIRouter) -> None:
        router.add_api_route(APIEndpoints.MENTIONED_STOCK.value, self.get_stock_data, methods=['GET'])
        router.add_api_route(APIEndpoints.CUSTOMER_STOCKS.value, self.get_customer_stocks, methods=['GET'])

    
    # async def get_stock_data(
    #     self, 
    #     request: Request,
    #     company: str = Query("Apple", description="Company name to analyze")
    # ) -> Dict:
    #     # Create and initialize controller
    #     controller = IDChatController()
    #     try:
    #         await controller.initialize()
    #         result = await controller.get_stock_data(company)
    #         return result
    #     finally:
    #         # Ensure controller is properly closed
    #         await controller.close()
            
    async def get_stock_data(
        self, 
        request: Request,
        company: str = Query("Apple", description="Company name to analyze")
    ) -> Dict:
        # Create and initialize controller
        # Define the path to your JSON file
        file_path = os.path.join(os.path.dirname(__file__), '../../data/mentioned_stock.json')
        
        try:
            # Open and read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return {"error": "Customer stocks file not found", "status": "error"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format in customer stocks file", "status": "error"}

            
                   
    async def get_customer_stocks(
        self, 
        request: Request,
        company: str = Query("Apple", description="Company name to analyze")
    ) -> Dict:
        """
        Read and return the content of customer_stocks.json file
        
        Args:
            request: FastAPI request object
            company: Company name to analyze (default: Apple)
            
        Returns:
            Dict: The contents of the customer_stocks.json file
        """
        # Define the path to your JSON file
        file_path = os.path.join(os.path.dirname(__file__), '../../data/customer_stocks.json')
        
        try:
            # Open and read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return {"error": "Customer stocks file not found", "status": "error"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format in customer stocks file", "status": "error"}

