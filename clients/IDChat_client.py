import aiohttp
import asyncio
import json
import pandas as pd
from urllib.parse import quote

class IDChatClient:
    """Simple client for interacting with the IDChat Agent API asynchronously."""
    
    def __init__(self):
        self.base_url = "https://idchat-api-containerapp01-dev.orangepebble-16234c4b.switzerlandnorth.azurecontainerapps.io"
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def ensure_session(self):
        """Ensure a session exists."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    async def query(self, query_str):
        """Query the graph with a natural language query."""
        await self.ensure_session()
        url = f"{self.base_url}/query?query={quote(query_str)}"
        async with self.session.post(url) as response:
            return await response.json()
    
    async def search_with_criteria(self, query_str):
        """Search companies that fulfill several criteria."""
        await self.ensure_session()
        url = f"{self.base_url}/searchwithcriteria?query={quote(query_str)}"
        async with self.session.post(url) as response:
            return await response.json()
    
    async def ohlcv(self, query_str, first="01.01.2024", last=None):
        """Get historical price data."""
        await self.ensure_session()
        url = f"{self.base_url}/ohlcv?query={quote(query_str)}&first={quote(first)}"
        if last:
            url = f"{url}&last={quote(last)}"
        async with self.session.post(url) as response:
            return await response.json()
    
    async def company_data_search(self, query_str):
        """Get information about one or more companies."""
        await self.ensure_session()
        url = f"{self.base_url}/companydatasearch?query={quote("company:{query_str}")}"
        async with self.session.post(url) as response:
            return await response.json()
    
    async def summary(self, query_str):
        """Get basic information about a company."""
        await self.ensure_session()
        url = f"{self.base_url}/summary?query={quote(query_str)}"
        async with self.session.post(url) as response:
            return await response.json()
    
    async def llm(self, query_str):
        """Query OpenAI 4o model."""
        await self.ensure_session()
        url = f"{self.base_url}/llm?query={quote(query_str)}"
        async with self.session.post(url) as response:
            return await response.json()
    
    def parse_table_data(self, response):
        """Helper method to parse table data from a response."""
        try:
            return pd.read_json(json.loads(response['messages'][2]['item'])['data'][0])
        except (KeyError, IndexError, json.JSONDecodeError):
            print("Could not parse table data from response")
            return None

# Example usage with multiple calls
async def main():
    async with IDChatClient() as client:
        # Make multiple calls and gather them
        tesla_task = client.query("Tesla between 2020 and 2022")
        apple_task = client.query("Apple between 2020 and 2022")

        # Await all results
        
        print("Tesla data:")
        print(await tesla_task)
        print("\nApple data:")
        print(await apple_task)


if __name__ == "__main__":
    asyncio.run(main())