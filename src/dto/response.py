from pydantic import BaseModel
from typing import Optional, Union
from ..database.models import Message

class ApiResponse(BaseModel):
    message: Optional[str] = ""
    data: Union[dict, str, list, None] = None

class ChatSchema(BaseModel):
    id: int
    title: str
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True

class TextObject(BaseModel):
    text: str = ""

class MessageSchema(BaseModel):
    role: str
    parts: list[TextObject]

    @classmethod
    def to_message_schema(cls, message: Message):
        return MessageSchema(
            role=str(message.role),
            parts=[TextObject(text=str(message.text))]
        )
