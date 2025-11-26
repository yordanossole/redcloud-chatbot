from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import user_route, chat_route, file_route

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_route.router, prefix="/api/user")
app.include_router(chat_route.router, prefix="/api/chat")
# app.include_router(file_route.router, prefix="/api/files")
