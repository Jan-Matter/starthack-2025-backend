import logging
import os
import traceback
from controllers.IDChat_controller import IDChatController
from controllers.text_interpreter_controller import TextInterpreterController

class ServiceInitializer:
    def __init__(self):
        self.customer_id = None
        self.id_chat_controller = None
        self.text_interpreter = None
        
    def set_customer_id(self, customer_id):
        self.customer_id = customer_id
        
    async def initialize(self, logger: logging.Logger):
        """Initialize services and start background tasks"""
        try:
            # Initialize IDChatController first
            logger.info("===== Initializing IDChat controller =====")
            self.id_chat_controller = IDChatController()
            await self.id_chat_controller.initialize()
            logger.info("===== IDChat controller initialized successfully =====")
            
            # Create the data directory if it doesn't exist
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            os.makedirs(data_dir, exist_ok=True)
            logger.info(f"Data directory: {data_dir}")
            
            # Ensure conversation.txt exists (it should based on your attachment)
            conversation_file = os.path.join(data_dir, 'conversation.txt')
            logger.info(f"Conversation file: {conversation_file} (exists: {os.path.exists(conversation_file)})")
            
            # Then initialize TextInterpreterController with the IDChatController
            logger.info("===== Initializing Text interpreter controller =====")
            
            # Explicitly check if id_chat_controller is properly initialized
            if not self.id_chat_controller or not hasattr(self.id_chat_controller, 'get_stock_data'):
                logger.error("IDChat controller is not properly initialized!")
                # Re-initialize as a last resort
                self.id_chat_controller = IDChatController()
                await self.id_chat_controller.initialize()
            
            self.text_interpreter = TextInterpreterController(
                data_dir=data_dir,
                id_chat_controller=self.id_chat_controller
            )
            await self.text_interpreter.start(logger)
            logger.info("===== Text interpreter controller started successfully =====")
            
        except Exception as e:
            logger.error(f"Error during service initialization: {str(e)}")
            logger.error(traceback.format_exc())
            raise