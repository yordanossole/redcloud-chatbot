from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
from ..config import GEMINI_API_KEY, GEMINI_API_MODEL
from ..database.models import get_db
from ..dto.response import ApiResponse, ChatSchema, MessageSchema
from ..database.db import get_chat, get_all_chats, create_new_chat, update_chat, delete_chat, get_user, get_messages, create_message
from ..custom_exceptions import GeneralException
from ..services.auth_service import validate_session_token


import json
from google import genai
from google.genai import types

router = APIRouter()

client = genai.Client(api_key=GEMINI_API_KEY)

@router.post("/create-chat")
async def create_chat(request: Request, db: Session = Depends(get_db)):
    try:
        session_token = request.cookies.get("session_token")
        if not session_token:
            return JSONResponse(status_code=401, content=ApiResponse(message="Not authenticated", data={}).model_dump())
        
        user = get_user(db=db, session_token=session_token)
        if user and not validate_session_token(db=db, username=str(user.username), token=session_token):
            return JSONResponse(status_code=401, content=ApiResponse(message="Invalid session", data={}).model_dump())

        new_chat = create_new_chat(db=db, user=user)
        api_response = ApiResponse(message="", data={ "chat_id": new_chat.id })
        response = JSONResponse(status_code=201, content=api_response.model_dump())
        return response
    except GeneralException as e:
        api_response = ApiResponse(message=e.message, data={})
        return JSONResponse(status_code=400, content=api_response.model_dump())
        
@router.get("/get-all-chats")
async def get_all_chats_route(request: Request, db: Session = Depends(get_db)):
    try:
        session_token = request.cookies.get("session_token")
        if not session_token:
            return JSONResponse(status_code=401, content=ApiResponse(message="Not authenticated", data={}).model_dump())
    
        user = get_user(db=db, session_token=session_token)
        if user and not validate_session_token(db=db, username=str(user.username), token=session_token):
            return JSONResponse(status_code=401, content=ApiResponse(message="Invalid session", data={}).model_dump())

        chats = get_all_chats(db=db, user=user)
        chats_schema = [ChatSchema.from_orm(chat) for chat in chats]
        api_response = ApiResponse(message="", data={"chats": chats_schema})
        response = JSONResponse(status_code=200, content=api_response.model_dump())
        return response
    except GeneralException as e:
        api_response = ApiResponse(message=e.message, data={})
        return JSONResponse(status_code=404, content=api_response.model_dump())

@router.get("/get-chat/{id}")
async def get_chat_messages_by_chat_id(chat_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        session_token = request.cookies.get("session_token")
        if not session_token:
            return JSONResponse(status_code=401, content=ApiResponse(message="Not authenticated", data={}).model_dump())
        
        user = get_user(db=db, session_token=session_token)
        if user and not validate_session_token(db=db, username=str(user.username), token=session_token):
            return JSONResponse(status_code=401, content=ApiResponse(message="Invalid session", data={}).model_dump())

        chat = get_chat(db=db, chat_id=chat_id, user=user)
        messages = get_messages(db=db, chat=chat)
        messages_schema = [MessageSchema.to_message_schema(message=message) for message in messages]
        api_response = ApiResponse(message="", data=messages_schema)
        response = JSONResponse(status_code=200, content=api_response.model_dump())
        return response
    except GeneralException as e:
        api_response = ApiResponse(message=e.message, data={})
        return JSONResponse(status_code=404, content=api_response.model_dump())
            

@router.post("/generate-response")
async def generate_response(request: Request, chat_id: int, question: str = "", db: Session = Depends(get_db)):
    try:
        db = next(get_db())
        session_token = request.cookies.get("session_token")
        if not session_token:
            return JSONResponse(status_code=401, content=ApiResponse(message="Not authenticated", data={}).model_dump())
        
        user = get_user(db=db, session_token=session_token)
        if user and not validate_session_token(db=db, username=str(user.username), token=session_token):
            return JSONResponse(status_code=401, content=ApiResponse(message="Invalid session", data={}).model_dump())

        chat = get_chat(db=db, chat_id=chat_id, user=user)
        messages = get_messages(db=db, chat=chat)
        messages_schema = [MessageSchema.to_message_schema(message).model_dump() for message in messages]

        chat_bot = client.chats.create(model=GEMINI_API_MODEL, history=messages_schema)
        response = chat_bot.send_message(question)
        content = str(response.text)

        new_bot_request = create_message(db=db, chat=chat, role="user", text=question)
        new_bot_response = create_message(db=db, chat=chat, role="model", text=content)

        api_response = ApiResponse(message="Chat model responded successfully", data=content)
        response = JSONResponse(status_code=200, content=api_response.model_dump())
        return response
    except GeneralException as e:
        api_response = ApiResponse(message=e.message, data={})
        return JSONResponse(status_code=400, content=api_response.model_dump())
