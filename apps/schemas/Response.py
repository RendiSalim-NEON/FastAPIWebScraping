from pydantic import BaseModel
from typing import Dict

class BaseResponse(BaseModel):
    status: int = 200
    message: str = None
    data: Dict = {}