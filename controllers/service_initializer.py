import logging
import asyncio
from controllers.Customer_controller import CustomerController

class ServiceInitializer:
    def __init__(self):
        self.initialized = False
        self.controllers = {}
        self.customer_id = "c007"  # Default customer ID
    
    # Remove the customer_id parameter completely from this method
    async def initialize(self, logger: logging.Logger):
        """
        Initialize all services with the stored customer ID
        
        Args:
            logger: The logger to use
        """
        try:
            logger.info(f"Initializing service controllers for customer ID: {self.customer_id}")
            
            # Initialize CustomerController with the stored customer_id
            customer_controller = CustomerController()
            await customer_controller.initialize(self.customer_id)
            self.controllers["Customer"] = customer_controller
            
            # Add other controllers as needed
            
            self.initialized = True
            logger.info("Service controllers initialized")
        except Exception as e:
            logger.error(f"Failed to initialize service controllers: {str(e)}")
            raise e
    
    # Create a new method specifically for setting the customer ID
    def set_customer_id(self, customer_id: str):
        """Set the customer ID to use during initialization"""
        self.customer_id = customer_id
        return self
    
    def get_controller(self, name):
        if not self.initialized:
            raise RuntimeError("Service not initialized")
        return self.controllers.get(name)
    
    async def shutdown(self):
        """Clean up resources on shutdown"""
        for name, controller in self.controllers.items():
            await controller.close()