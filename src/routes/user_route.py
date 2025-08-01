from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..config import SESSION_EXPIRY_MINUTES
from ..services.auth_service import verify_user, create_session_token, create_new_user, delete_session
from ..database.models import get_db
from ..dto.request import CreateUserRequest
from ..dto.response import ApiResponse
from ..custom_exceptions import GeneralException


router = APIRouter()

@router.post('/login')
async def sign_in(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        if not verify_user(db, create_user_request.username, create_user_request.password):
            raise GeneralException(message="Incorrect username or password")

        token = create_session_token(db, create_user_request.username)

        api_response_model = ApiResponse(message="Logged in successfully", data={})
        response = JSONResponse(status_code=200, content=api_response_model.model_dump())
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            max_age=SESSION_EXPIRY_MINUTES * 60,
            secure=False,
            samesite="lax"
        )

        return response
    except GeneralException as e:
        api_response = ApiResponse(message=e.message, data={})
        return JSONResponse(status_code=401, content=api_response.model_dump())

@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    try:
        token = str(request.cookies.get("session_token", "No token"))
        print(f"\n\n\n\n\n{token}\n\n\n\n------")
        user = delete_session(db=db, session_token=token)
        # response.delete_cookie("session_token")
        api_response = ApiResponse(message=f"{user.username} logged out successfully", data={})

        response = JSONResponse(status_code=200, content=api_response.model_dump())
        response.delete_cookie("session_token")
        return response
    except GeneralException as e:
        api_response = ApiResponse(message=e.message, data={})
        return JSONResponse(status_code=400, content=api_response.model_dump())


@router.post("/sign-up")
async def sign_up(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        user = create_new_user(db=db, username=create_user_request.username, password=create_user_request.password)

        token = create_session_token(db, create_user_request.username)
        api_response = ApiResponse(message=f"{user.username} sign-up successful", data={})

        response = JSONResponse(status_code=201, content=api_response.model_dump())
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            max_age=SESSION_EXPIRY_MINUTES * 60,
            secure=False,
            samesite="lax"
        )
        return response
    except GeneralException as e:
        api_response = ApiResponse(message=e.message, data={})
        return JSONResponse(status_code=400, content=api_response.model_dump())
