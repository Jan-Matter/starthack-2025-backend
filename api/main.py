import uvicorn
from fastapi import FastAPI, APIRouter, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging
import argparse
import watchtower
import boto3
import os
from controllers.service_initializer import ServiceInitializer

from api.routes.liveness import Liveness
from api.routes.fininfo import Fininfo

from api.constants import APIEndpoints, LoggingMessages, Env
from clients.s3_client import S3FileStore

async def background_function():
    logger.info("Running startup tasks...")
    # Only pass logger to initialize
    service_initializer = ServiceInitializer()
    await service_initializer.initialize(logger)
    logger.info("Startup tasks completed")

def create_app(
    logger: logging.Logger,
    filestore: S3FileStore,
    env: str,
    customer_id: str
    ) -> FastAPI:
    
    app = FastAPI(
        docs_url=APIEndpoints.DOCS.value,
        redoc_url=APIEndpoints.REDOC.value,
        openapi_url=APIEndpoints.OPENAPI_URL.value
    )
    
    #cors settings
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    router = APIRouter()
    
    liveness_route = Liveness()
    logger.info("Adding liveness routes")
    liveness_route.add_api_routes(router)
    logger.info("Added liveness routes")
    
    
    fininfo_route = Fininfo()
    logger.info("Adding fininfo routes")
    fininfo_route.add_api_routes(router)
    logger.info("Added fininfo routes")
    
    
    app.include_router(router)


    background_task = BackgroundTasks()
    background_task.add_task(background_function)
    app.add_event_handler("startup", background_task)        
    
    logger.info(LoggingMessages.API_READY.value)
    
    
    return app


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Start the API server')
    # Add customer_id argument
    parser.add_argument('--customer_id', type=str, default='c007', 
                      help='Customer ID to process (default: c007)')
    args = parser.parse_args()

    ENV = os.getenv('ENV', 'test')
    FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    

    filestore = S3FileStore()  
    logger = logging.getLogger('guhring-api')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(FORMAT)
    
    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"
    #cloudwatch logger
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        log_group='starthack',
        stream_name=f'starthack-{ENV}',
        use_queues=False #required otherwise handler shuts down in uvicorn
    )
    cloudwatch_handler.setLevel(logging.INFO)
    cloudwatch_handler.setFormatter(formatter)
    logger.addHandler(cloudwatch_handler)
    
    #console logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
        
    try:
        app = create_app(
            logger=logger,
            filestore=filestore,
            env=ENV,
            customer_id=args.customer_id  # Pass the customer_id
            )
    except Exception as e:
        logger.error("An error occurred during startup")
        logger.error(e)
        raise e
    
    
    uvicorn.run(
        app, 
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
        access_log=False
    )