import json
import os
import logging
from pathlib import Path
from controllers.IDChat_controller import IDChatController

class CustomerController:
    def __init__(self):
        self.customers_data = None
        self.file_path = os.path.join(os.path.dirname(__file__), '../data/customer.json')
        self.stocks_file_path = os.path.join(os.path.dirname(__file__), '../data/customer_stocks.json')
        self.idchat_controller = None
        
    async def initialize(self, customer_id="c007"):
        """
        Initialize the controller by loading customer data and saving stocks for specified customer
        
        Args:
            customer_id (str): The ID of the customer to process (default: c007)
        """
        try:
            await self.load_customer_data()
            # Initialize IDChatController
            self.idchat_controller = IDChatController()
            await self.idchat_controller.initialize()
            # Call method with the provided customer ID
            await self.save_customer_stocks(customer_id)
        except Exception as e:
            logging.error(f"Failed to initialize CustomerController: {str(e)}")
            raise
            
    async def load_customer_data(self):
        """Load customer data from the JSON file"""
        try:
            with open(self.file_path, 'r') as file:
                self.customers_data = json.load(file)
            logging.info("Customer data loaded successfully")
        except Exception as e:
            logging.error(f"Error loading customer data: {str(e)}")
            raise
    
    def get_customer_by_id(self, customer_id):
        """Retrieve customer information by ID"""
        if not self.customers_data:
            raise RuntimeError("Customer data not loaded. Initialize controller first.")
            
        for customer in self.customers_data.get("customers", []):
            if customer.get("id") == customer_id:
                return customer
                
        return None
    
    def get_customer_companies(self, customer_id):
        """
        Retrieve a list of companies that a customer has invested in
        
        Args:
            customer_id (str): The ID of the customer
        
        Returns:
            list: A list of company names
        """
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return []
            
        # Extract company names from investments
        companies = []
        for investment in customer.get("investments", []):
            companies.append(investment.get("company"))
            
        return companies
    
    def save_customer_companies_to_json(self, customer_id):
        """
        Save a customer's invested companies to a JSON file
        
        Args:
            customer_id (str): The ID of the customer
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            companies = self.get_customer_companies(customer_id)
            customer = self.get_customer_by_id(customer_id)
            
            if not customer:
                logging.error(f"Customer with ID {customer_id} not found")
                return False
                
            data = {
                "customer_id": customer_id,
                "customer_name": customer.get("name"),
                "companies": companies
            }
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.stocks_file_path), exist_ok=True)
            
            # Write to JSON file
            with open(self.stocks_file_path, 'w') as file:
                json.dump(data, file, indent=2)
                
            logging.info(f"Successfully wrote company data for customer {customer_id} to {self.stocks_file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error saving customer companies to JSON: {str(e)}")
            return False
    
    async def save_customer_stocks(self, customer_id):
        """
        Save comparison data for specified customer's companies using IDChatController
        
        Args:
            customer_id (str): The ID of the customer
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            companies = self.get_customer_companies(customer_id)
            
            if not companies:
                logging.error(f"No companies found for customer {customer_id}")
                return False
                
            # Use IDChatController to get comparison data
            if not self.idchat_controller:
                logging.error("IDChatController not initialized")
                return False
                
            logging.info(f"Getting comparison data for companies: {companies}")
            comparison_result = await self.idchat_controller.compare_companies(
                companies=companies,
                metric="market_cap"
            )
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.stocks_file_path), exist_ok=True)
            
            # Write the comparison result to JSON file
            with open(self.stocks_file_path, 'w') as file:
                json.dump(comparison_result, file, indent=2)
                
            logging.info(f"Successfully saved comparison data for customer {customer_id} to {self.stocks_file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error saving comparison data to JSON: {str(e)}")
            return False
            
    async def close(self):
        """Clean up resources"""
        if self.idchat_controller:
            await self.idchat_controller.close()
