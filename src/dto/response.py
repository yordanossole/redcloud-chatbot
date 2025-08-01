from pydantic import BaseModel
from typing import Optional

class ApiResponse(BaseModel):
    message: Optional[str] = ""
    data: Optional[dict] = None