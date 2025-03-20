from enum import Enum


HEALTHY = "healthy"
UNHEALTHY = "unhealthy"

class APIEndpoints(Enum):
    LIVENESS = "/api/v1/healthy"
    DOCS = "/api/v1/docs"
    REDOC = "/api/v1/redoc"
    OPENAPI_URL = "/api/v1/openapi.json"
    

class Env(Enum):
    test = "test"
    prod = "prod"


class LoggingMessages(Enum):
    API_READY = "API is ready"


