from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from core.doc import convert_document
from urllib.parse import quote
import io
import zipfile
import base64

def content_disposition(filename: str) -> str:
    ascii_name = filename.encode('ascii', errors='ignore').decode()
    encoded_name = quote(filename)
    if ascii_name == filename:
        return f'attachment; filename="{filename}"'
    return f"attachment; filename*=UTF-8''{encoded_name}"

router = APIRouter()

@router.post("/convert")
async def convert(file: UploadFile = File(...)):
    data = await file.read()
    filename = file.filename or "document"
    result = convert_document(data, filename)
    # 统一返回 JSON，前端负责预览和打包下载
    return JSONResponse({
        "markdown": result.get("markdown", ""),
        "images": result.get("images", []),
        "filename": filename,
    })
