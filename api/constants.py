from enum import Enum


HEALTHY = "healthy"
UNHEALTHY = "unhealthy"

class APIEndpoints(Enum):
    LIVENESS = "/api/v1/healthy"
    DOCS = "/api/v1/docs"
    REDOC = "/api/v1/redoc"
    OPENAPI_URL = "/api/v1/openapi.json"
    WEBSOCKET_AUDIO_RECV = "/api/v1/ws/audio_recv"
    

class Env(Enum):
    test = "test"
    prod = "prod"


class LoggingMessages(Enum):
    API_READY = "API is ready"
    ERROR_RECEIVING_AUDIO_DATA = "Error receiving audio data: "
    SOCKET_LISTENING = "Socket listening on port "


