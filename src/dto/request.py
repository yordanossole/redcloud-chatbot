from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateUserRequest(BaseModel):
    username: str
    password: str
    

class UpdateUserBase(BaseModel):
    username: str = ""
    password: str = ""
    session_token: str = ""
    token_expiry: Optional[datetime] = None

