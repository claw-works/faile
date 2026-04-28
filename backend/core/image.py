from PIL import Image
import io

FORMAT_MAP = {
    "webp": ("image/webp", "WEBP"),
    "jpg": ("image/jpeg", "JPEG"),
    "jpeg": ("image/jpeg", "JPEG"),
    "png": ("image/png", "PNG"),
}

def process_image(data: bytes, width=None, height=None, crop=None, format="webp", quality=85):
    img = Image.open(io.BytesIO(data))
    if img.mode in ("RGBA", "P") and format in ("jpg", "jpeg"):
        img = img.convert("RGB")

    if crop:
        x, y, w, h = crop
        img = img.crop((x, y, x + w, y + h))

    if width or height:
        orig_w, orig_h = img.size
        if width and not height:
            height = int(orig_h * width / orig_w)
        elif height and not width:
            width = int(orig_w * height / orig_h)
        img = img.resize((width, height), Image.LANCZOS)

    mime, fmt = FORMAT_MAP.get(format.lower(), ("image/webp", "WEBP"))
    buf = io.BytesIO()
    save_kwargs = {"quality": quality} if fmt != "PNG" else {}
    img.save(buf, format=fmt, **save_kwargs)
    return buf.getvalue(), mime

def get_image_info(data: bytes):
    img = Image.open(io.BytesIO(data))
    return {"width": img.width, "height": img.height, "mode": img.mode, "format": img.format}
