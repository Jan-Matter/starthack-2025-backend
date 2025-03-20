import os
import logging
import json
import re
import asyncio
from typing import Optional, Dict, Any

class TextInterpreterController:
    def __init__(self, data_dir=None, id_chat_controller=None):
        """
        Initialize the Text Interpreter Controller.
        
        Args:
            data_dir (str, optional): Directory where conversation.txt is located
            id_chat_controller: Controller for getting stock data
        """
        # Use absolute path based on file location if data_dir not provided
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        else:
            self.data_dir = data_dir
            
        self.conversation_file = "conversation.txt"
        self.stock_file = "mentioned_stock.json"
        self.logger = None
        self.is_running = False
        self.task = None
        self.id_chat_controller = id_chat_controller
        
        # List of common company names to check against
        self.company_names = [
            "Apple", "Microsoft", "Amazon", "Google", "Facebook", "Meta", 
            "Tesla", "Netflix", "Nvidia", "Intel", "AMD", "IBM", "Oracle", 
            "Salesforce", "Adobe", "PayPal", "Uber", "Airbnb", "Twitter", 
            "Snapchat", "Spotify", "Disney", "Walmart", "Target", "Costco", 
            "Nike", "Coca-Cola", "Pepsi", "McDonald's", "Starbucks"
        ]
        
    async def start(self, logger: Optional[logging.Logger] = None):
        """
        Start the text interpreter controller to run every 5 seconds.
        
        Args:
            logger: Logger instance to use for logging
        """
        if self.is_running:
            return
            
        self.logger = logger or logging.getLogger(__name__)
        self.is_running = True
        self.logger.info("Starting Text Interpreter Controller")
        
        # Run immediately on startup
        await self.process_conversation()
        
        # Then create background task to run every 5 seconds
        self.task = asyncio.create_task(self._run_periodically())
        
    async def _run_periodically(self):
        """Background task that runs the processor every 5 seconds"""
        while self.is_running:
            await asyncio.sleep(5)  # Wait for 5 seconds
            await self.process_conversation()
    
    async def stop(self):
        """Stop the periodic processing"""
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.task = None
        
    async def process_conversation(self):
        """Process the conversation file and extract company information"""
        try:
            parsed_data = await self.parse_conversation()
            if parsed_data and parsed_data.get("mentioned_companies"):
                self.logger.info(f"Found companies: {parsed_data['mentioned_companies']}")
            return parsed_data
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error processing conversation: {e}")
            return None
        
    def read_conversation(self):
        """
        Reads the conversation.txt file from the data directory.
        
        Returns:
            str: The content of the conversation.txt file
            None: If file could not be read
        """
        try:
            file_path = os.path.join(self.data_dir, self.conversation_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading conversation file: {e}")
            return None
            
    async def parse_conversation(self, content=None):
        """
        Parse the conversation content. If no content is provided,
        the method will read the conversation file first.
        
        Args:
            content (str, optional): The conversation content to parse.
            
        Returns:
            dict: Parsed conversation data
        """
        if content is None:
            content = self.read_conversation()
            
        if content is None:
            return None
            
        # Find mentioned companies
        mentioned_companies = self.extract_company_names(content)
        
        # Save to JSON if companies found
        if mentioned_companies:
            await self.save_mentioned_stocks(mentioned_companies)
            
        return {
            "raw_text": content,
            "length": len(content),
            "mentioned_companies": mentioned_companies
        }
    
    def extract_company_names(self, text):
        """
        Extract company names from text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            list: List of identified company names
        """
        mentioned_companies = []
        
        for company in self.company_names:
            # Use regex with word boundaries to find whole words
            pattern = r'\b' + re.escape(company) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                mentioned_companies.append(company)
                
        return mentioned_companies
    
    async def save_mentioned_stocks(self, companies):
        """
        Save mentioned companies to the mentioned_stock.json file.
        Uses get_stock_data to retrieve stock information.
        
        Args:
            companies (list): List of company names to save
        """
        try:
            if not companies:
                if self.logger:
                    self.logger.warning("No companies to save")
                return
                
            # Ensure the directory exists
            os.makedirs(self.data_dir, exist_ok=True)
            output_file = os.path.join(self.data_dir, self.stock_file)
            
            # Use first mentioned company
            company_name = companies[0] if companies else ""
            
            if self.id_chat_controller is None:
                if self.logger:
                    self.logger.error("IDChat controller is not initialized")
                return
                
            if not company_name:
                if self.logger:
                    self.logger.warning("No company name provided")
                return
                
            # Use the controller to get stock data
            if self.logger:
                self.logger.info(f"Getting stock data for company: {company_name}")
            
            # Set date range (last year to now)
            start_date = "20.03.2024"
            end_date = "20.03.2025"
            
            # Call the get_stock_data method directly
            try:
                stock_data = await self.id_chat_controller.get_stock_data(
                    company_name=company_name,
                    start_date=start_date,
                    end_date=end_date
                )
                
                # Write the stock data to JSON file
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(stock_data, file, indent=4)
                    
                if self.logger:
                    self.logger.info(f"Successfully saved stock data for {company_name} to {output_file}")
                    
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error getting stock data: {str(e)}")
                    
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error in save_mentioned_stocks: {str(e)}")
                import traceback
                self.logger.error(traceback.format_exc())

# Add to your service_initializer.py file
from controllers.text_interpreter_controller import TextInterpreterController

class ServiceInitializer:
    def __init__(self):
        self.customer_id = None
        self.text_interpreter = TextInterpreterController()
        
    def set_customer_id(self, customer_id):
        self.customer_id = customer_id
        
    async def initialize(self, logger):
        """Initialize services and start background tasks"""
        # Your existing initialization code...
        
        # Start the text interpreter controller
        await self.text_interpreter.start(logger)
        logger.info("Text interpreter controller started")
        
        # Rest of your initialization code...