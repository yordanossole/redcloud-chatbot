# from fastapi import APIRouter, Depends, Request
# from fastapi.responses import JSONResponse
# from sqlalchemy.orm import Session
# from ..services.chat_service import build_and_save_index
# from ..dto.response import ApiResponse
# from ..database.models import get_db

# router = APIRouter()

# @router.post("/process-doc")
# async def process_documents(db: Session = Depends(get_db)):
#     try:
#         build_and_save_index()
#         api_response = ApiResponse(message="Build and Save Index and Documents Sucessfull", data={})
#         response = JSONResponse(status_code=200, content=api_response.model_dump())
#         return response
#     except Exception as e:
#         api_response = ApiResponse(message=f"Error occured while processing documents. \n{e}", data={})
#         response = JSONResponse(status_code=500, content=api_response.model_dump())
#         return response

# @router.post("/upload-file")
# async def upload_files():
#     return ApiResponse(message="On process", data={})

# @router.get("/all")
# async def get_all_files():
#     return ApiResponse(message="On process", data={})

# @router.get("/{file_name}")
# async def get_file_by_id(file_name: str):
#     return ApiResponse(message="On process", data={})

# @router.delete("/{file_name}")
# async def delete_file_by_id(file_name: str):
#     return ApiResponse(message="On process", data={})