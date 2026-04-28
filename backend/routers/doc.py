from fastapi import APIRouter, UploadFile, File
from core.doc import convert_document

router = APIRouter()

@router.post("/convert")
async def convert(file: UploadFile = File(...)):
    data = await file.read()
    filename = file.filename or ""
    result = convert_document(data, filename)
    return result
