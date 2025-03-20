from fastapi import APIRouter, Request
from typing import Dict

from api.constants import APIEndpoints
from api.schemas.liveness import LivenessResponse


class Liveness:

    def __init__(self) -> None:
        pass
    
    def add_api_routes(self, router: APIRouter) -> None:
        router.add_api_route(APIEndpoints.LIVENESS.value, self.get, methods=['GET'])
    
    async def get(self, request: Request) -> Dict:
        return LivenessResponse(status="healthy")