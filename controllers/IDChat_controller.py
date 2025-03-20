import sys
import os
import asyncio
import json
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Any, Optional, Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clients.IDChat_client import IDChatClient

class IDChatController:
    """Controller for handling IDChat client operations and processing the results."""
    
    def __init__(self):
        self.client = None
    
    async def initialize(self):
        """Initialize the client if it doesn't exist."""
        if self.client is None:
            self.client = IDChatClient()
            await self.client.ensure_session()
        return self
    
    async def close(self):
        """Close the client session if it exists."""
        if hasattr(self, 'client') and self.client and self.client.session:
            await self.client.session.close()
    
    async def get_company_summary(self, company_name: str) -> Dict[str, Any]:
        """Get a summary of company information."""
        await self.initialize()
        
        try:
            result = await self.client.summary(company_name)
            # Process the result as needed
            return {
                "company": company_name,
                "data": result,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {
                "company": company_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    async def get_stock_data(self, company_name: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Get historical stock data for a company."""
        await self.initialize()
        
        if not start_date:
            # Default to 1 year ago
            start_date = (datetime.now() - timedelta(days=365)).strftime("%d.%m.%Y")
        
        if not end_date:
            end_date = datetime.now().strftime("%d.%m.%Y")
        
        try:
            result = await self.client.ohlcv(company_name, first=start_date, last=end_date)
            
            # Try to parse table data if available
            table_data = self.client.parse_table_data(result)
            
            return {
                "company": company_name,
                "period": f"{start_date} to {end_date}",
                "data": result,
                "parsed_data": table_data.to_dict() if isinstance(table_data, pd.DataFrame) else None,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {
                "company": company_name,
                "period": f"{start_date} to {end_date}",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    async def compare_companies(self, companies: List[str], metric: str = None) -> Dict[str, Any]:
        """Compare multiple companies based on optional metrics."""
        await self.initialize()
        
        tasks = []
        for company in companies:
            # Get company data
            tasks.append(self.client.company_data_search(company))
        
        try:
            results = await asyncio.gather(*tasks)
            
            processed_results = {}
            for i, company in enumerate(companies):
                processed_results[company] = results[i]
            
            # If a specific metric was requested, extract and compare it
            compared_data = {}
            if metric:
                for company, data in processed_results.items():
                    # Extract the metric from data (this would need customization based on response structure)
                    compared_data[company] = self._extract_metric(data, metric)
            
            return {
                "companies": companies,
                "metric": metric,
                "data": processed_results,
                "comparison": compared_data if metric else None,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {
                "companies": companies,
                "metric": metric,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    async def search_companies_by_criteria(self, criteria: str) -> Dict[str, Any]:
        """Search for companies matching specific criteria."""
        await self.initialize()
        
        try:
            result = await self.client.search_with_criteria(criteria)
            
            return {
                "criteria": criteria,
                "data": result,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {
                "criteria": criteria,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    async def get_market_insights(self, query: str) -> Dict[str, Any]:
        """Get market insights using the LLM functionality."""
        await self.initialize()
        
        try:
            result = await self.client.llm(query)
            
            return {
                "query": query,
                "data": result,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    async def get_comprehensive_company_profile(self, company_name: str) -> Dict[str, Any]:
        """Get a comprehensive profile of a company by combining multiple data sources."""
        await self.initialize()
        
        # Create tasks for different data sources
        summary_task = self.client.summary(company_name)
        stock_task = self.client.ohlcv(company_name)
        details_task = self.client.company_data_search(company_name)
        
        try:
            # Execute all tasks concurrently
            summary_result, stock_result, details_result = await asyncio.gather(
                summary_task, stock_task, details_task
            )
            
            # Process the stock data if available
            stock_data = self.client.parse_table_data(stock_result)
            
            return {
                "company": company_name,
                "summary": summary_result,
                "stock_data": stock_result,
                "stock_table": stock_data.to_dict() if isinstance(stock_data, pd.DataFrame) else None,
                "details": details_result,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {
                "company": company_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def _extract_metric(self, data: Dict[str, Any], metric: str) -> Any:
        """Helper method to extract a specific metric from company data."""
        # This would need to be customized based on the structure of the data
        # Simple example implementation:
        try:
            # Assuming data has a structure like {messages: [{item: "..."}]}
            for message in data.get('messages', []):
                if 'item' in message:
                    item_data = json.loads(message['item'])
                    if metric in item_data:
                        return item_data[metric]
            return None
        except Exception:
            return None

# Example of how to use the controller
async def example_usage():
    controller = IDChatController()
    try:
        await controller.initialize()
        
        # Example: Get a comprehensive profile
        result = await controller.get_comprehensive_company_profile("Apple")
        print(json.dumps(result, indent=2))
        
        # Example: Compare companies
        comparison = await controller.compare_companies(["Apple", "Microsoft", "Google"], "market_cap")
        print(json.dumps(comparison, indent=2))
        
    finally:
        await controller.close()

if __name__ == "__main__":
    asyncio.run(example_usage())