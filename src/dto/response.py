from pydantic import BaseModel
from typing import Optional, Union

class ApiResponse(BaseModel):
    message: Optional[str] = ""
    data: Union[dict, str, None] = None