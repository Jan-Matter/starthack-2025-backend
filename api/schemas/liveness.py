from pydantic import BaseModel
from typing import Literal

class LivenessResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]