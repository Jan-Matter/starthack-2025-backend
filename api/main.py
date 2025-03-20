import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging
import argparse
import watchtower
import boto3
import os


from api.routes.liveness import Liveness
from api.constants import APIEndpoints, LoggingMessages, Env
from clients.s3_client import S3FileStore
    

def create_app(
    logger: logging.Logger,
    filestore: S3FileStore,
    env: str
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
    
    app.include_router(router)
    
    logger.info(LoggingMessages.API_READY.value)
    
    return app


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Start the API server')
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
            env=ENV
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