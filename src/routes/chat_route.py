from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
from ..config import GEMINI_API_KEY, GEMINI_API_MODEL
from ..database.models import get_db
from ..dto.response import ApiResponse


import json
from google import genai
from google.genai import types

router = APIRouter()

client = genai.Client(api_key=GEMINI_API_KEY)

@router.post("/generate-response")
async def generate_response(db: Session = Depends(get_db), question: Optional[str] = ""):
    try:
        chat = client.chats.create(model=GEMINI_API_MODEL)
        response = chat.send_message(question)
        content = str(response.text)

        api_response = ApiResponse(message="Chat model responded successfully", data=content).model_dump()
        response = JSONResponse(status_code=200, content=api_response)
        return response
    except Exception as e:
        api_response = ApiResponse(message="Chat model has got error", data=str(e)).model_dump()
        return JSONResponse(status_code=400, content=api_response)
