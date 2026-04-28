from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response
from core.image import process_image, get_image_info
from typing import Optional
import json

router = APIRouter()

@router.post("/process")
async def process(
    file: UploadFile = File(...),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    crop_x: Optional[int] = Form(None),
    crop_y: Optional[int] = Form(None),
    crop_w: Optional[int] = Form(None),
    crop_h: Optional[int] = Form(None),
    format: str = Form("webp"),
    quality: int = Form(85),
):
    data = await file.read()
    crop = (crop_x, crop_y, crop_w, crop_h) if all(v is not None for v in [crop_x, crop_y, crop_w, crop_h]) else None
    result, mime = process_image(data, width=width, height=height, crop=crop, format=format, quality=quality)
    return Response(content=result, media_type=mime)

@router.post("/info")
async def info(file: UploadFile = File(...)):
    data = await file.read()
    return get_image_info(data)
