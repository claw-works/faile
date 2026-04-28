from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from core.doc import convert_document
import io
import zipfile

router = APIRouter()

@router.post("/convert")
async def convert(file: UploadFile = File(...)):
    data = await file.read()
    filename = file.filename or "document"
    result = convert_document(data, filename)

    # 如果只有 markdown 没有图片，直接返回 .md 文件
    if not result.get("images"):
        md_bytes = result["markdown"].encode("utf-8")
        return StreamingResponse(
            io.BytesIO(md_bytes),
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="document.md"'},
        )

    # 有图片就打包成 zip
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("document.md", result["markdown"])
        for img in result["images"]:
            import base64
            zf.writestr(f"images/{img['filename']}", base64.b64decode(img["base64"]))
    buf.seek(0)

    stem = filename.rsplit(".", 1)[0]
    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{stem}.zip"'},
    )
